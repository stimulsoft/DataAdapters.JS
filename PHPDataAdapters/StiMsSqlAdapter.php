<?php
# Stimulsoft.Reports.JS
# Version: 2024.3.6
# Build date: 2024.09.19
# License: https://www.stimulsoft.com/en/licensing/reports
?>
<?php

namespace Stimulsoft\Adapters;

use Stimulsoft\StiDataResult;
use Stimulsoft\StiResult;

class StiMsSqlAdapter extends StiDataAdapter
{
    public $version = '2024.3.6';
    public $checkVersion = true;

    protected $driverName = 'sqlsrv';

    protected function getLastErrorResult($message = 'An unknown error has occurred.')
    {
        if ($this->driverType == 'PDO')
            return parent::getLastErrorResult($message);

        $code = 0;

        if ($this->driverType == 'Microsoft') {
            if (($errors = sqlsrv_errors()) != null) {
                $error = $errors[count($errors) - 1];
                $code = $error['code'];
                $message = $error['message'];
            }
        }
        else {
            $error = mssql_get_last_message();
            if ($error) $message = $error;
        }

        return $code == 0 ? StiResult::error($message) : StiResult::error("[$code] $message");
    }

    protected function connect()
    {
        if ($this->driverType == 'PDO')
            return parent::connect();

        if ($this->driverType == 'Microsoft') {
            if (!function_exists('sqlsrv_connect'))
                return StiResult::error('MS SQL driver not found. Please configure your PHP server to work with MS SQL.');

            sqlsrv_configure('WarningsReturnAsErrors', 0);
            $this->connectionLink = sqlsrv_connect(
                $this->connectionInfo->host,
                array(
                    'UID' => $this->connectionInfo->userId,
                    'PWD' => $this->connectionInfo->password,
                    'Database' => $this->connectionInfo->database,
                    'LoginTimeout' => 10,
                    'ReturnDatesAsStrings' => true,
                    'CharacterSet' => $this->connectionInfo->charset
                ));

            if (!$this->connectionLink)
                return $this->getLastErrorResult();

            return StiDataResult::success();
        }

        $this->connectionLink = mssql_connect($this->connectionInfo->host, $this->connectionInfo->userId, $this->connectionInfo->password);
        if (!$this->connectionLink)
            return $this->getLastErrorResult();

        if (!mssql_select_db($this->connectionInfo->database, $this->connectionLink))
            return $this->getLastErrorResult();

        return StiResult::success();
    }

    protected function disconnect()
    {
        if ($this->driverType == 'PDO')
            parent::disconnect();
        else if ($this->connectionLink) {
            if ($this->driverType == 'Microsoft')
                sqlsrv_close($this->connectionLink);
            else
                mssql_close($this->connectionLink);

            $this->connectionLink = null;
        }
    }

    public function parse($connectionString)
    {
        if (parent::parse($connectionString))
            return true;

        $this->driverType = function_exists('mssql_connect') ? 'Native' : 'Microsoft';
        $this->connectionInfo->charset = 'UTF-8';

        $parameterNames = array(
            'host' => ['server', 'data source'],
            'database' => ['database', 'initial catalog', 'dbname'],
            'userId' => ['uid', 'user', 'user id'],
            'password' => ['pwd', 'password'],
            'charset' => ['charset']
        );

        return $this->parseParameters($parameterNames);
    }

    private function getStringType($type)
    {
        switch ($type) {
            case -6:
            case -5:
            case 4:
            case 5:
                return 'int';

            case 2:
            case 3:
            case 6:
            case 7:
                return 'decimal';

            case -7:
                return 'bit';

            case 91:
            case 93:
                return 'datetime';

            case -155:
                return 'datetimeoffset';

            case -154:
                return 'time';

            case -152:
            case -11:
            case -10:
            case -9:
            case -8:
            case -2:
            case -1:
            case 1:
            case 12:
                return 'string';

            case -151:
                return 'geometry'; // 'udt'

            case -150:
            case -4:
            case -3:
                return 'binary';
        }

        return 'string';
    }

    protected function parseType($meta)
    {
        if ($this->driverType == 'PDO') {
            $type = $meta['sqlsrv:decl_type'];
            //$length = $meta['len'];
        }
        else {
            $type = $this->getStringType($meta['Type']);
            //$length = $meta['Size'];
        }

        switch ($type) {
            case 'bigint':
            case 'int':
            case 'smallint':
            case 'tinyint':
                return 'int';

            case 'decimal':
            case 'float':
            case 'money':
            case 'numeric':
            case 'real':
            case 'smallmoney':
                return 'number';

            case 'bit':
                return 'boolean';

            case 'char':
            case 'nchar':
            case 'ntext':
            case 'nvarchar':
            case 'text':
            case 'timestamp':
            case 'uniqueidentifier':
            case 'varchar':
            case 'xml':
                return 'string';

            case 'date':
            case 'datetime':
            case 'datetime2':
            case 'smalldatetime':
                return 'datetime';

            case 'datetimeoffset':
                return 'datetimeoffset';

            case 'time':
                return 'time';

            case 'binary':
            case 'image':
            case 'sql_variant':
            case 'varbinary':
            case 'cursor':
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

            case 'datetimeoffset':
                $offset = substr($value, strpos($value, '+'));
                $value = substr($value, 0, strpos($value, '+'));
                $timestamp = strtotime($value);
                $format = date("Y-m-d\TH:i:s.v", $timestamp);
                if (strpos($format, '.v') > 0) $format = date("Y-m-d\TH:i:s.000", $timestamp);
                return $format . $offset;

            case 'time':
                $timestamp = strtotime($value);
                $format = date("H:i:s.v", $timestamp);
                if (strpos($format, '.v') > 0) $format = date("H:i:s.000", $timestamp);
                return $format;
        }

        return $value;
    }

    public function makeQuery($procedure, $parameters)
    {
        $paramsString = parent::makeQuery($procedure, $parameters);
        return "EXEC $procedure $paramsString";
    }

    protected function executeNative($queryString, $result)
    {
        $query = $this->driverType == 'Microsoft'
            ? sqlsrv_query($this->connectionLink, $queryString)
            : mssql_query($queryString, $this->connectionLink);

        if (!$query)
            return $this->getLastErrorResult();

        if ($this->driverType == 'Microsoft') {
            foreach (sqlsrv_field_metadata($query) as $meta) {
                $result->columns[] = $meta['Name'];
                $result->types[] = $this->parseType($meta);
            }
        }

        $isColumnsEmpty = count($result->columns) == 0;
        while ($rowItem = ($this->driverType == 'Microsoft'
            ? sqlsrv_fetch_array($query, $isColumnsEmpty ? SQLSRV_FETCH_ASSOC : SQLSRV_FETCH_NUMERIC)
            : mssql_fetch_assoc($query))) {

            $row = array();
            foreach ($rowItem as $key => $value) {
                if ($isColumnsEmpty && count($result->columns) < count($rowItem)) $result->columns[] = $key;
                $type = count($result->types) >= count($row) + 1 ? $result->types[count($row)] : 'string';
                $row[] = $this->getValue($type, $value);
            }
            $result->rows[] = $row;
        }

        return $result;
    }
}