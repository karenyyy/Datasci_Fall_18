<?php

require_once(__DIR__.'/../config/connect.php');

$REGEX_NUMBER='/\d+/';
$REGEX_WORD = '/[a-zA-Z]+/';

/**
 * @param $datechar
 * edit date format to be MySQL compatible
 * Dec 01 2018 --> 2018-12-01
 * @return string
 */
function edit_date($datechar){

    $year = substr($datechar, -4);
    $month = substr($datechar, 0, 3);
    $day = substr($datechar, -7, 2);

    if ($month=='Jan'){
        $month = '01';
    }else{
        $month = '12';
    }

    $date_ymd =  implode('-', array($year, $month, $day));
    return $date_ymd;
}


/**
 * @param $time
 * extract the start time of a shift
 * @return int
 */
function edit_time($time){
    global $REGEX_NUMBER, $REGEX_WORD;

    $start_time_ampm = explode('-', $time)[0]; // 7AM/3PM/11PM

    preg_match($REGEX_NUMBER, $start_time_ampm,$match_hour);
    preg_match($REGEX_WORD, $start_time_ampm,$match_ampm);
    $start_time = $match_hour[0];

    if ($match_ampm[0] == 'PM'){
        $start_time +=12;
    }
    return $start_time;
}


/**
 * preferred shift start time extract: 11PM --> 23; 7AM -- 7
 */
function edit_employee_table(){
    global $db;
    $query = "SELECT * FROM employee";
    $result_set = mysqli_query($db, $query);

    while ($result = mysqli_fetch_assoc($result_set)) {
        $empid = $result['empid'];

        // convert the format of preferred shift time
        $start_time = edit_time($result['preferred_shift']);
        $query = "UPDATE employee SET pre_shift_start = $start_time WHERE empid = $empid";
        mysqli_query($db, $query);

    }
}

/**
 * drop unnecessary columns
 */
function drop_cols_employee(){
    global $db;
    $query = "ALTER TABLE employee DROP COLUMN preferred_shift;";
    mysqli_query($db,$query);
}


/**
 * date format convert: Dec 01 2018 --> 2018-12-01
 * shift start time extract: 11PM --> 23; 7AM -- 7
 */
function edit_need_table(){
    global $db;
    $query = "SELECT needid,datechar,shiftchar FROM need";
    $result_set = mysqli_query($db, $query);

    while ($result = mysqli_fetch_assoc($result_set)) {
        $needid = $result['needid'];

        // convert the format of date
        $date = edit_date($result['datechar']);
        $query = "UPDATE need SET date = '$date' where needid=$needid";
        mysqli_query($db, $query);

        // convert the format of shift time
        $start_time = edit_time($result['shiftchar']);
        $query = "UPDATE need SET start_time = $start_time WHERE needid = $needid";
        mysqli_query($db, $query);

    }
}

/**
 * drop unnecessary columns
 */
function drop_cols_need(){
    global $db;
    $query = "ALTER TABLE need DROP COLUMN datechar";
    mysqli_query($db, $query);
}


/**
 * replace (firstname, lastname) with empid
 * convert date format
 */
function edit_dayoff_table(){
    global $db;
    $query = "SELECT * FROM day_off";
    $result_set = mysqli_query($db, $query);

    while ($result = mysqli_fetch_assoc($result_set)) {
        $offid = $result['offid'];
        $firstname = $result['firstName'];
        $lastname = $result['lastName'];

        # replace (firstname, lastname) with empid
        $query = "
            UPDATE day_off SET empid = (SELECT empid FROM employee b
                            WHERE b.firstName= '$firstname'
                            AND b.lastName= '$lastname')
            WHERE offid = $offid";

        mysqli_query($db, $query);

        # convert date format
        $date = edit_date($result['datechar']);
        $query = "UPDATE day_off SET date = '$date' where offid=$offid";
        mysqli_query($db, $query);
    }
}


/**
 * drop unnecessary columns
 */
function drop_cols_dayoff(){
    global $db;
    $query = "ALTER TABLE day_off DROP COLUMN firstName";
    mysqli_query($db, $query);
    $query = "ALTER TABLE day_off DROP COLUMN lastName";
    mysqli_query($db, $query);
    $query = "ALTER TABLE day_off DROP COLUMN datechar";
    mysqli_query($db, $query);
}


/**
 * add a table to keep track of the available counts for each employee
 */
function add_available_cnt_table(){
    global $db;
    $query = "
        CREATE TABLE IF NOT EXISTS employee_available_shift_count
            (
                empid int not null ,
                available_shifts_cnt int not null
            ) select e2.empid,
                     if(e2.ftpt='FT', 10-e2.daysoff, 6-e2.daysoff) as available_shifts_cnt
              from (select e.empid, e.ftpt, e.firstName, e.lastName,
                           if(d.daysoff, d.daysoff, 0) as daysoff
                    from employee e
                             left join
                             (select empid, count(*) as daysoff
                              from day_off group by empid) d
                             on e.empid=d.empid) e2;
    ";
    mysqli_query($db, $query);

}


function edit_tables()
{

     edit_employee_table();
     drop_cols_employee();
     edit_need_table();
     drop_cols_need();
     edit_dayoff_table();
     drop_cols_dayoff();
     add_available_cnt_table();
}

