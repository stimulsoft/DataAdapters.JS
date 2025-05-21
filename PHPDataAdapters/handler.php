<?php
# Stimulsoft.Reports.JS
# Version: 2025.2.4
# Build date: 2025.05.19
# License: https://www.stimulsoft.com/en/licensing/reports
?>
<?php

use Stimulsoft\StiBaseHandler;
use Stimulsoft\Events\StiDataEventArgs;

// Event handler classes and functions.
require_once 'enums\StiBaseEventType.php';
require_once 'enums\StiDataCommand.php';
require_once 'enums\StiDataType.php';
require_once 'enums\StiDatabaseType.php';
require_once 'events\StiEvent.php';
require_once 'events\StiEventArgs.php';
require_once 'events\StiConnectionEventArgs.php';
require_once 'events\StiDataEventArgs.php';
require_once 'classes\StiConnectionInfo.php';
require_once 'classes\StiFunctions.php';
require_once 'classes\StiBaseRequest.php';
require_once 'classes\StiBaseResult.php';
require_once 'classes\StiDataResult.php';
require_once 'classes\StiBaseResponse.php';
require_once 'classes\StiBaseHandler.php';
require_once 'classes\StiPath.php';
require_once 'classes\StiParameter.php';

// Data adapters for supported database types.
require_once 'StiDataAdapter.php';
require_once 'StiFileAdapter.php';
require_once 'StiXmlAdapter.php';
require_once 'StiJsonAdapter.php';
require_once 'StiCsvAdapter.php';
require_once 'StiSqlAdapter.php';
require_once 'StiFirebirdAdapter.php';
require_once 'StiMongoDbAdapter.php';
require_once 'StiMsSqlAdapter.php';
require_once 'StiMySqlAdapter.php';
require_once 'StiOdbcAdapter.php';
require_once 'StiOracleAdapter.php';
require_once 'StiPostgreSqlAdapter.php';

// You can configure the security level as you required.
// By default is to allow any requests from any domains.
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept, Engaged-Auth-Token');
header('Cache-Control: no-cache');

// Processing database connection parameters.
$onBeginProcessData = function (StiDataEventArgs $args) {
    
};

// Creating the data handler and assign events.
$handler = new StiBaseHandler();
$handler->onBeginProcessData->append($onBeginProcessData);

// Processing the request.
// If the parameter 'true' is passed, all results will be output, otherwise only the data necessary for the adapters.
$handler->process(true);