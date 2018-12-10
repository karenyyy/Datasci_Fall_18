<?php

require_once(__DIR__.'/../config/connect.php');
require_once ('schedule_single_employee.php');

/**
 * schedule for all department in the department need table order by the number of employees needed;
 */
function schedule_all(){
    global $db;
    // departments with larger number of needed employees have higher priority to be get scheduled
    $query = "SELECT * FROM need ORDER BY emp_need desc, needid desc";
    $result_set = mysqli_query($db, $query);
    while ($result = mysqli_fetch_assoc($result_set)) {
        $num_emp_needed_each_dept = $result['emp_need'];
        while ($num_emp_needed_each_dept >= 1) {
            $success_or_not = schedule_someone($result['dept'],
                                                $result['date'],
                                                $result['start_time'],
                                                $result['emptype']);
            if ($success_or_not = 0) {
                echo "<br />" . "Something is wrong with needid = " . $result['needid'] . "<br />";
            }
            $num_emp_needed_each_dept -= 1;
        }
        echo "<br />" . "No more employee needed!" . "<br />";

    }
}