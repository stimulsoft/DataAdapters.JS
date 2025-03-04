<?php
# Stimulsoft.Reports.JS
# Version: 2025.1.6
# Build date: 2025.02.28
# License: https://www.stimulsoft.com/en/licensing/reports
?>
<?php

namespace Stimulsoft\Enums;

use Stimulsoft\StiFunctions;

class StiDataCommand
{
    const GetSupportedAdapters = 'GetSupportedAdapters';
    const TestConnection = 'TestConnection';
    const RetrieveSchema = 'RetrieveSchema';
    const Execute = 'Execute';
    const ExecuteQuery = 'ExecuteQuery';


### Helpers

    public static function getValues(): array
    {
        return StiFunctions::getConstants('Stimulsoft\Enums\StiDataCommand');
    }
}