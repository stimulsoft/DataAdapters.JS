<?php
# Stimulsoft.Reports.JS
# Version: 2024.1.1
# Build date: 2023.12.08
# License: https://www.stimulsoft.com/en/licensing/reports
?>
<?php

namespace Stimulsoft;

class StiDatabaseType
{
    const MySQL = 'MySQL';
    const MSSQL = 'MS SQL';
    const PostgreSQL = 'PostgreSQL';
    const Firebird = 'Firebird';
    const Oracle = 'Oracle';
    const ODBC = 'ODBC';
    const MongoDB = 'MongoDB';

    public static function getTypes() {
        $reflectionClass = new \ReflectionClass('\Stimulsoft\StiDatabaseType');
        $databases = $reflectionClass->getConstants();
        return array_values($databases);
    }
}