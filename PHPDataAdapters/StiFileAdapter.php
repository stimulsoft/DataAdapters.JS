<?php
# Stimulsoft.Reports.JS
# Version: 2025.2.1
# Build date: 2025.03.20
# License: https://www.stimulsoft.com/en/licensing/reports
?>
<?php

namespace Stimulsoft\Adapters;

use Exception;
use Stimulsoft\Enums\StiDataType;
use Stimulsoft\StiDataResult;
use Stimulsoft\StiPath;

class StiFileAdapter extends StiDataAdapter
{

### Properties

    /** @var string The data type loaded by the data adapter. */
    protected $dataType = StiDataType::Text;

    /** @var StiPath Link to the created database connection driver. */
    protected $connectionLink;


### Methods

    protected function connect(): StiDataResult
    {
        $path = new StiPath($this->connectionString, $this->handler->checkFileNames);
        if ($path->filePath == null)
            return StiDataResult::getError("Data file '$this->connectionString' not found.")->getDataAdapterResult($this);

        $this->connectionLink = $path;

        return StiDataResult::getSuccess()->getDataAdapterResult($this);
    }

    public function getDataResult($filePath, $maxDataRows = -1): StiDataResult
    {
        $this->connectionString = $filePath;
        $this->process();

        $result = $this->connect();
        if ($result->success) {
            try {
                $result->data = file_get_contents($this->connectionLink->filePath);
                $result->dataType = $this->dataType;
            }
            catch (Exception $e) {
                $message = $e->getMessage();
                $result = StiDataResult::getError($message)->getDataAdapterResult($this);
            }
        }

        return $result;
    }
}