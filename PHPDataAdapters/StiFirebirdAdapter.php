<?php
# Stimulsoft.Reports.JS
# Version: 2024.3.5
# Build date: 2024.09.04
# License: https://www.stimulsoft.com/en/licensing/reports
?>
<?php

namespace Stimulsoft\Adapters;

use Stimulsoft\StiDataResult;
use Stimulsoft\StiResult;

class StiFirebirdAdapter extends StiDataAdapter
{
    public $version = '2024.3.5';
    public $checkVersion = true;

    protected $driverName = 'firebird';

    protected function getLastErrorResult($message = 'An unknown error has occurred.')
    {
        if ($this->driverType == 'PDO')
            return parent::getLastErrorResult($message);

        $code = ibase_errcode();
        $error = ibase_errmsg();
        if ($error) $message = $error;

        return $code == 0 ? StiResult::error($message) : StiResult::error("[$code] $message");
    }

    protected function connect()
    {
        if ($this->driverType == 'PDO')
            return parent::connect();

        if (!function_exists('ibase_connect'))
            return StiResult::error('Firebird driver not found. Please configure your PHP server to work with Firebird.');

        $this->connectionLink = ibase_connect(
            $this->connectionInfo->host . '/' . $this->connectionInfo->port . ':' . $this->connectionInfo->database,
            $this->connectionInfo->userId, $this->connectionInfo->password, $this->connectionInfo->charset);
        if (!$this->connectionLink)
            return $this->getLastErrorResult();

        return StiDataResult::success();
    }

    protected function disconnect()
    {
        if ($this->driverType == 'PDO')
            parent::disconnect();
        else if ($this->connectionLink) {
            ibase_close($this->connectionLink);
            $this->connectionLink = null;
        }
    }

    public function parse($connectionString)
    {
        if (parent::parse($connectionString))
            return true;

        $this->connectionInfo->port = 3050;
        $this->connectionInfo->charset = 'UTF8';

        $parameterNames = array(
            'host' => ['server', 'host', 'location', 'datasource', 'data source'],
            'port' => ['port'],
            'database' => ['database', 'dbname'],
            'userId' => ['uid', 'user', 'username', 'userid', 'user id'],
            'password' => ['pwd', 'password'],
            'charset' => ['charset']
        );

        return $this->parseParameters($parameterNames);
    }

    protected function parseType($meta)
    {
        switch ($meta) {
            case 'SMALLINT':
            case 'INTEGER':
            case 'BIGINT':
                return 'int';

            case 'FLOAT':
            case 'DOUBLE PRECISION':
            case 'NUMERIC':
            case 'DECIMAL':
                return 'number';

            case 'DATE':
            case 'TIMESTAMP':
                return 'datetime';

            case 'TIME':
                return 'time';

            case 'CHAR':
            case 'VARCHAR':
                return 'string';

            case 'BLOB':
                return 'array';
        }

        return 'string';
    }

    protected function getValue($type, $value)
    {
        if (is_null($value) || strlen($value) == 0)
            return null;

        switch ($type) {
            case 'array':
                return base64_encode($value);

            case 'datetime':
                $timestamp = strtotime($value);
                $format = date("Y-m-d\TH:i:s.v", $timestamp);
                if (strpos($format, '.v') > 0) $format = date("Y-m-d\TH:i:s.000", $timestamp);
                return $format;

            case 'time':
                $timestamp = strtotime($value);
                $format = date("H:i:s.v", $timestamp);
                if (strpos($format, '.v') > 0) $format = date("H:i:s.000", $timestamp);
                return $format;

            case 'string':
                return mb_convert_encoding($value, 'UTF-8', mb_list_encodings());
        }

        return $value;
    }

    public function makeQuery($procedure, $parameters)
    {
        $paramsString = parent::makeQuery($procedure, $parameters);
        return "EXECUTE PROCEDURE $procedure $paramsString";
    }

    protected function executeNative($queryString, $result)
    {
        $query = ibase_query($this->connectionLink, $queryString);
        if (!$query)
            return $this->getLastErrorResult();

        $result->count = ibase_num_fields($query);

        for ($i = 0; $i < $result->count; $i++) {
            $meta = ibase_field_info($query, $i);
            $result->columns[] = $meta['name'];
            $result->types[] = $this->parseType($meta['type']);
        }

        while ($rowItem = ibase_fetch_assoc($query, IBASE_TEXT)) {
            $row = array();
            foreach ($rowItem as $value) {
                $type = count($result->types) >= count($row) + 1 ? $result->types[count($row)] : 'string';
                $row[] = $this->getValue($type, $value);
            }
            $result->rows[] = $row;
        }

        return $result;
    }

    protected function executePDO($queryString, $result)
    {
        // PDO Firebird driver doesn't support getColumnMeta()
        // The type is determined by the first value

        return $this->executePDOv2($queryString, $result);
    }
}