<?php
# Stimulsoft.Reports.JS
# Version: 2025.2.1
# Build date: 2025.03.20
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