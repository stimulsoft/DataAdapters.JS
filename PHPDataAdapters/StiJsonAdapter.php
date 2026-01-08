<?php
# Stimulsoft.Reports.JS
# Version: 2026.1.2
# Build date: 2026.01.06
# License: https://www.stimulsoft.com/en/licensing/reports
?>
<?php

namespace Stimulsoft\Adapters;

use Stimulsoft\Enums\StiDatabaseType;
use Stimulsoft\Enums\StiDataType;

class StiJsonAdapter extends StiFileAdapter
{

### Properties

    /** @var string Current version of the data adapter. */
    public $version = '2026.1.2';

    /** @var bool Sets the version matching check on the server and client sides. */
    public $checkVersion = true;

    protected $type = StiDatabaseType::JSON;
    protected $dataType = StiDataType::JSON;

}