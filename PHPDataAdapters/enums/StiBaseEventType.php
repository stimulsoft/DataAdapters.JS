<?php
# Stimulsoft.Reports.JS
# Version: 2025.2.4
# Build date: 2025.05.19
# License: https://www.stimulsoft.com/en/licensing/reports
?>
<?php

namespace Stimulsoft\Enums;

use Stimulsoft\StiFunctions;

class StiBaseEventType
{
    const DatabaseConnect = 'DatabaseConnect';
    const BeginProcessData = 'BeginProcessData';
    const EndProcessData = 'EndProcessData';


### Helpers

    public static function getValues(): array
    {
        return StiFunctions::getConstants('Stimulsoft\Enums\StiBaseEventType');
    }
}