<?php
# Stimulsoft.Reports.JS
# Version: 2024.2.2
# Build date: 2024.03.11
# License: https://www.stimulsoft.com/en/licensing/reports
?>
<?php

namespace Stimulsoft;

class StiDataResult extends StiResult
{
    public $types;
    public $columns;
    public $rows;
    public $count;

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