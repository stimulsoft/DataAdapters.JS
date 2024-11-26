<?php
# Stimulsoft.Reports.JS
# Version: 2024.4.5
# Build date: 2024.11.22
# License: https://www.stimulsoft.com/en/licensing/reports
?>
<?php

namespace Stimulsoft\Enums;

use Stimulsoft\StiFunctions;

class StiDatabaseType
{
    const MySQL = 'MySQL';
    const MSSQL = 'MS SQL';
    const PostgreSQL = 'PostgreSQL';
    const Firebird = 'Firebird';
    const Oracle = 'Oracle';
    const ODBC = 'ODBC';
    const MongoDB = 'MongoDB';


### Helpers

    public static function getValues(): array
    {
        return StiFunctions::getConstants('Stimulsoft\Enums\StiDatabaseType');
    }
}