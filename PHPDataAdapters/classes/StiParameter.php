<?php
# Stimulsoft.Reports.JS
# Version: 2025.2.4
# Build date: 2025.05.19
# License: https://www.stimulsoft.com/en/licensing/reports
?>
<?php

namespace Stimulsoft;

class StiParameter
{

### Properties

    /** @var string The name of the parameter. */
    public $name = null;

    /** @var int The type code of the parameter. */
    public $typeCode = null;

    /** @var string The type name of the parameter. */
    public $typeName = null;

    /** @var string The type group of the parameter. */
    public $typeGroup = null;

    /** @var int The size of the parameter. */
    public $size = null;

    /** @var object The value of the parameter. The type of object depends on the type of parameter. */
    public $value = null;


### Constructor

    public function __construct(string $name, int $typeCode, string $typeName, string $typeGroup, int $size, $value)
    {
        $this->name = $name;
        $this->typeCode = $typeCode;
        $this->typeName = $typeName;
        $this->typeGroup = $typeGroup;
        $this->size = $size;
        $this->value = $value;
    }
}