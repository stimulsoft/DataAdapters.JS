<?php
# Stimulsoft.Reports.JS
# Version: 2026.2.3
# Build date: 2026.05.21
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