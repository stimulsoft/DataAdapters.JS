<?php
# Stimulsoft.Reports.JS
# Version: 2026.1.2
# Build date: 2026.01.06
# License: https://www.stimulsoft.com/en/licensing/reports
?>
<?php

namespace Stimulsoft\Enums;

use Stimulsoft\StiFunctions;

class StiDatabaseType
{
    // File
    const XML = 'XML';
    const JSON = 'JSON';
    const CSV = 'CSV';

    // SQL
    const MySQL = 'MySQL';
    const MSSQL = 'MS SQL';
    const PostgreSQL = 'PostgreSQL';
    const Firebird = 'Firebird';
    const Oracle = 'Oracle';
    const ODBC = 'ODBC';

    // NoSQL
    const MongoDB = 'MongoDB';


### Helpers

    public static function getValues(): array
    {
        return StiFunctions::getConstants('Stimulsoft\Enums\StiDatabaseType');
    }
}