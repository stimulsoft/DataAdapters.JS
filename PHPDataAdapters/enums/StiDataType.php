<?php
# Stimulsoft.Reports.JS
# Version: 2025.2.2
# Build date: 2025.04.08
# License: https://www.stimulsoft.com/en/licensing/reports
?>
<?php

namespace Stimulsoft\Enums;

use Stimulsoft\StiFunctions;

class StiDataType
{
    const JavaScript = "text/javascript";
    const JSON = "application/json";
    const XML = "application/xml";
    const HTML = "text/html";
    const CSV = "text/csv";
    const Text = "text/plain";


### Helpers

    public static function getValues(): array
    {
        return StiFunctions::getConstants("Stimulsoft\Enums\StiDataType");
    }
}