<?php

require_once('config/connect.php');
require_once ('util/preprocess.php');
require_once ('util/draw_report.php');
require_once ('schedule/schedule_for_department.php');
require_once('report/employee/report_happiness.php');
require_once('report/employee/report_cost.php');
require_once('report/employee/report_unused_shift_and_utilization.php');
require_once('report/department/report_unfilled_needs.php');
require_once('report/employee/report_all_info_of_employees.php');


$time_start = microtime(true);


//Create connection
$db = db_connect();


###################################################################
########################## Tasks ##################################
###################################################################

edit_tables();  // Total Execution Time: 4.0263858159383 mins
schedule_all();  // Total Execution Time: 4.6495327313741 mins
//cal_total_cost();
//

###################################################################
########################## Visualization ##########################
###################################################################

create_happiness_report();
create_unused_shift_and_utilization_report();
create_unfilled_needs_report();
create_all_report();  // Total Execution Time: 0.0015837669372559 mins

$time_end = microtime(true);

$execution_time = ($time_end - $time_start)/60;
echo '<h3>Total Execution Time: '.$execution_time.' mins</h3>';


//Disconnect
db_disconnect($db);

?>
