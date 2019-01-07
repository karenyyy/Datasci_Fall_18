<?php

require_once(__DIR__.'/../config/connect.php');


/**
 * @param $dept
 * @param $date
 * @param $start_time
 * @param $emptype
 * process:
 *      1. check if this need exists
 *      2. get available employees
 *      3. schedule this employee
 *      4. update department need
 *      5. update available shift count
 * @return int
 */
function schedule_someone($dept, $date, $start_time, $emptype)
{
    global $db;

    ###################################################################
    ################ check if this need exists ########################
    ###################################################################

    $query = "      
            SELECT * FROM need 
            WHERE dept = '$dept'
            AND date = '$date'
            AND start_time = $start_time
            AND emptype = '$emptype';               
            ";
    $result_set = mysqli_query($db, $query);
    if (mysqli_num_rows($result_set) < 1) {
        echo "<br />" . "There is no such a need!" . "<br />";
        return 0;
    }
    $result_need = mysqli_fetch_assoc($result_set);
    $needid = $result_need['needid'];
    $num_of_employees_needed = $result_need['emp_need'];

    if ($num_of_employees_needed < 1) {
        echo "<br />" . "No more employee needed!" . "<br />";
        return 0;
    }


    ###################################################################
    ################ get available employees ##########################
    ###################################################################

    $query = "
            SELECT empid, emptype from (
                SELECT e.empid,
                       e.emptype,
                       e.ftpt,
                       e.pre_shift_start,
                       e.dept_cert,
                       e.wage,
                       easc.available_shifts_cnt FROM employee e
                inner join employee_available_shift_count easc
                on e.empid = easc.empid) tmp
                WHERE emptype = '$emptype' AND locate('$dept', dept_cert)>0
                  AND empid NOT IN
                      (SELECT empid FROM day_off
                       WHERE date = '$date')
                  AND empid NOT IN
                      (SELECT empid FROM schedule
                       WHERE date = '$date')
                  AND available_shifts_cnt > 0
                ORDER BY ftpt, if(abs(pre_shift_start-23)=0, pre_shift_start-23, 1), wage
            ";
    $result_set = mysqli_query($db, $query);

    if (!$result_set) {
        echo "<br />" ."There is no employee meets this condition!" ."<br />";
        return 0;
    }
    $result = mysqli_fetch_assoc($result_set);
    $num_candidates=mysqli_num_rows($result_set);
    while ($num_candidates>=1) {
        $empid = $result['empid'];
        $query = "SELECT DAYOFWEEK('$date') AS dayoffweek";

        $result_dayofweeek = mysqli_fetch_assoc(mysqli_query($db, $query));

        // not weekend
        if ($result_dayofweeek['dayoffweek'] != 1 and $result_dayofweeek['dayoffweek'] != 7) {
            //echo 'Not weekend!';
            //echo '<br>';
            break;
        }

        // weekend
        //// if the request day = Sunday:
        if ($result_dayofweeek['dayoffweek'] == 1) {
            //echo 'yes Sunday';
            //echo '<br>';
            $query = "
                SELECT COUNT(*) AS exist FROM schedule
                WHERE empid = $empid
                AND date = date_sub('$date', interval 1 day);
                ";
        }
        //// if the request day = Saturday:
        if ($result_dayofweeek['dayoffweek'] == 7) {
            //echo 'yes Saturday';
            //echo '<br>';
            $query = "
                SELECT COUNT(*) AS exist FROM schedule
                WHERE empid = $empid
                AND date = date_add('$date', interval 1 day)
                ";
        }
        //echo $query;
        //echo '<br>';
        $weekend_scheduled = mysqli_fetch_assoc(mysqli_query($db, $query));

        if ($weekend_scheduled['exist'] == 0) {
            // weekend not scheduled, available for schedule
            //echo 'yes weekend not scheduled';
            //echo '<br>';
            break;
        } else {
            // weekend scheduled, not available for schedule, move on to the next one
            $result = mysqli_fetch_assoc($result_set);
            $num_candidates -= 1;
        }

    }
    //echo $result['empid'];
    //echo '<br>';
    // all available employee extracted after filtering dayoff requested and scheduled are occupied on weekends
    if ($num_candidates == 0) {
        echo "<br />" . "There is no employee meets this condition after considering!" . "<br />";
        return 0;
    }

    ###################################################################
    ################ schedule this employee ###########################
    ###################################################################

    $empid = $result['empid'];
    $query = "INSERT INTO schedule (date, empid, dept, start_time) 
              VALUES ('$date', $empid, '$dept', $start_time);";
    mysqli_query($db, $query);
    echo "Successfully schedule employee whose empid = " .$empid ." !" ."<br />";



    ###################################################################
    ################# update department need ##########################
    ###################################################################

    $query = "UPDATE need SET emp_need = (emp_need - 1) WHERE needid = $needid";
    mysqli_query($db, $query);

    ###################################################################
    ################# update available shift count ####################
    ###################################################################

    $query = "UPDATE employee_available_shift_count 
              SET available_shifts_cnt = (available_shifts_cnt - 1) 
              WHERE empid = $empid";
    mysqli_query($db, $query);

    return 1;
}

