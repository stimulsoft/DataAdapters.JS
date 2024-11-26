<?php
# Stimulsoft.Reports.JS
# Version: 2024.4.5
# Build date: 2024.11.22
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