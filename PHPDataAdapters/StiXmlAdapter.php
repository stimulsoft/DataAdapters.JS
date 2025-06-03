<?php
# Stimulsoft.Reports.JS
# Version: 2025.2.5
# Build date: 2025.06.02
# License: https://www.stimulsoft.com/en/licensing/reports
?>
<?php

namespace Stimulsoft\Adapters;

use Stimulsoft\Enums\StiDatabaseType;
use Stimulsoft\Enums\StiDataType;

class StiXmlAdapter extends StiFileAdapter
{

### Properties

    /** @var string Current version of the data adapter. */
    public $version = '2025.2.5';

    /** @var bool Sets the version matching check on the server and client sides. */
    public $checkVersion = true;

    protected $type = StiDatabaseType::XML;
    protected $dataType = StiDataType::XML;

}