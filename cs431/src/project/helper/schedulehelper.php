<?php
/**
 * Created by PhpStorm.
 * User: karen
 * Date: 10/22/18
 * Time: 3:09 PM
 */

require_once('../connect/connect.php');


function departmentList($con)
{
    $query = "SELECT department_name FROM department";
    $scrolldown_list = '';
    if (!($result = mysqli_query($con, $query))) {
        $msg = 'MySQL error #' . mysqli_connect_errno() . ": " . mysqli_connect_error();
        echo $msg;
    }else{
        while ($row = mysqli_fetch_assoc($result)) {
            foreach ($row as $dept) {
                $scrolldown_list = $scrolldown_list."<option value=\"$dept\"> $dept </option>";
            }
        }
        return $scrolldown_list;
    }

}


function shiftlenList($con, $start_time)
{
    $query = "SELECT length FROM shift WHERE from_time='$start_time'";
    $result = mysqli_query($con, $query);
    $scrolldown_list = '';
    if (!($result)) {
        $msg = 'MySQL error #' . mysqli_connect_errno() . ": " . mysqli_connect_error();
        echo $msg;
    }else{
        while ($row = mysqli_fetch_assoc($result)) {
            foreach ($row as $shiftlen) {
                $scrolldown_list = $scrolldown_list."<option value=\"$shiftlen\"> $shiftlen </option>";
            }
        }
        return $scrolldown_list;
    }
}


function startTimeList($con)
{
    $query = "SELECT DISTINCT from_time FROM shift";
    $result = mysqli_query($con, $query);
    $scrolldown_list = '';
    if (!($result)) {
        $msg = 'MySQL error #' . mysqli_connect_errno() . ": " . mysqli_connect_error();
        echo $msg;
    }else{
        while ($row = mysqli_fetch_assoc($result)) {
            foreach ($row as $from_time) {
                $scrolldown_list = $scrolldown_list."<option value=\"$from_time\"> $from_time </option>";
            }
        }
        return $scrolldown_list;
    }
}


function convert_date_format($date)
{
    $splitted_date = explode('-', $date);
    $month = $splitted_date[0];
    $day = $splitted_date[1];
    $year = $splitted_date[2];
    $new_date = implode('-', array($year, $month, $day));
    return $new_date;
}

