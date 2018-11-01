<?php
/**
 * Created by PhpStorm.
 * User: karen
 * Date: 10/12/18
 * Time: 9:23 PM
 */


require_once('../connect/connect.php');


if(isset($_POST['ScheduleID'])) {
    $ScheduleID = $_POST['ScheduleID'];

    $result = mysqli_query($con, "DELETE FROM schedule WHERE schedule_id=$ScheduleID");

    if ($result){
        echo 'unscheduled!';
    }
    header("Refresh:0");
}