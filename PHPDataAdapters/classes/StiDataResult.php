<?php
# Stimulsoft.Reports.JS
# Version: 2022.4.5
# Build date: 2022.11.15
# License: https://www.stimulsoft.com/en/licensing/reports
?>
<?php

namespace Stimulsoft;

class StiDataResult extends StiResult
{
    public $types;
    public $columns;
    public $rows;

    public static function success($notice = null, $object = null)
    {
        $result = new StiDataResult();
        $result->success = true;
        $result->notice = $notice;
        $result->object = $object;

        $result->types = array();
        $result->columns = array();
        $result->rows = array();

        return $result;
    }
}