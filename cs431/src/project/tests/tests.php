<link rel="stylesheet" type="text/css" HREF="../css/style.css">

<?php
/**
 * Created by PhpStorm.
 * User: karen
 * Date: 10/24/18
 * Time: 12:00 PM
 */

require_once('../connect/connect.php');
require_once('../helper/schedulehelper.php');


function insert($con, $dept, $date, $empid, $start_time, $firstname, $lastname)
{
    $query = "SELECT length FROM shift WHERE from_time='$start_time'";
    $res = mysqli_query($con, $query);
    $num_lengths = mysqli_num_rows($res);
    if ($num_lengths > 1) {
        echo '<h4><center>But there are multiple shift length at this start time!!</center></h4>';
        $i = 0;
        while ($row = mysqli_fetch_assoc($res)) {
            $i = $i + 1;
            echo '<center><br><br>option ' . $i . ':  ' . $row['length'] . 'hrs <br></center>';
        }
        echo '<br><br><center>Which shift length? Please specify!</center>';
    } else {
        $shift_length = mysqli_fetch_assoc($res)['length'];

        $query = "INSERT INTO schedule (date, empid, dept, start_time, shift_length) VALUES
                      ('$date',
                       '$empid',
                       '$dept',
                       '$start_time',
                        $shift_length)";
        echo '<center>SQL Query: ' . $query . '</center>';
        $result = mysqli_query($con, $query);
        if (!($result)) {
            $msg = 'MySQL error #' . mysqli_connect_errno() . ": " . mysqli_connect_error();
            printf($msg, __FILE__, __LINE__);
        } else {
            echo '<br><br><h4><center>Employee <i>' . $firstname . ' ' . $lastname . '</i> is scheduled on ' . $date . ' starting from ' . $start_time . ' for ' . $shift_length . ' hours in ' . $dept . '</center></h4>';
        }
    }
}


function schedule($con, $dept, $date, $empid, $start_time)
{
    $date = convert_date_format($date);

    $query = "SELECT firstname, lastname
                  FROM employees
                  WHERE empid = '$empid'";
    $result = mysqli_query($con, $query);

    if (0 == mysqli_num_rows($result)) {
        echo '<br><br>
                    <h4 style="color: red"><center>No Employee <i>' . $empid . '</i> in the database! Please double check!</center></h4>';
    } else {
        $row = mysqli_fetch_assoc($result);
        $firstname = $row['firstname'];
        $lastname = $row['lastname'];

        $query = "SELECT *
                FROM schedule
                WHERE empid='$empid'
                AND date='$date'
                AND dept='$dept'";

        $result = mysqli_query($con, $query);
        if (!($result)) {
            $msg = 'MySQL error #' . mysqli_connect_errno() . ": " . mysqli_connect_error();
            printf($msg, __FILE__, __LINE__);
        } else if (0 == mysqli_num_rows($result)) {

            echo '<br>
                    <h4><center><i>' . $firstname . ' ' . $lastname . '</i> is open for schedule on ' . $date . ' starting from ' . $start_time . ' in ' . $dept . ' </center></h4><br>';

            insert($con, $dept, $date, $empid, $start_time, $firstname, $lastname);
        } else {

            echo "<br><br>";
            echo "<h4 style='color: red'><center>Employee <i>" . $firstname . " " . $lastname . "</i> has already been scheduled on $date:</center></h4><br><br>";

            echo "<table class='center' border=1>";
            echo "<tr>";
            $i = 0;
            while ($i < mysqli_num_fields($result)) {
                $meta = mysqli_fetch_field_direct($result, $i);
                echo '<td>' . $meta->name . '</td>';
                $i = $i + 1;
            }

            while ($row = mysqli_fetch_assoc($result)) {
                echo "<tr>\n";
                foreach ($row as $cell) {
                    echo "<td> $cell </td>";
                }
                echo "</tr>\n";
            }

            echo "</table><br><br><br>";
        }
    }


}


function unschedule($con, $dept, $date, $empid)
{
    $date = convert_date_format($date);

    $query = "SELECT firstname, lastname
                  FROM employees
                  WHERE empid = '$empid'";
    $result = mysqli_query($con, $query);

    if (0 == mysqli_num_rows($result)) {
        echo '<br><br>
                    <h4 style="color: red"><center>No Employee <i>' . $empid . '</i> in the database! Please double check!</center></h4>';
    } else {
        $row = mysqli_fetch_assoc($result);

        $firstname = $row['firstname'];
        $lastname = $row['lastname'];


        $query = "SELECT *
                FROM schedule
                WHERE empid='$empid'
                AND date='$date'
                AND dept='$dept'";
        if (0 == mysqli_num_rows(mysqli_query($con, $query))) {

            echo '<br><br><center><h4 style="color: red">Employee <i>' . $firstname . ' ' . $lastname . '</i> has not been scheduled, please double check!!</h4></center><br>';
        } else {
            $query = "DELETE FROM schedule WHERE dept='$dept' AND date='$date' AND empid='$empid'";
            $result = mysqli_query($con, $query);
            if ($result) {
                echo '<center><h4>Employee <i>' . $firstname . ' ' . $lastname . '</i> is successfully unscheduled on ' . $date . ' in the ' . $dept . ' department.</h4></center><br><br>';
            }
        }
    }
}

function test_cases($con)
{
    $dept_arr = array('EMERGENCY', 'PEDIATRICS', 'RADIOLOGY', 'ONCOLOGY');
    $empid_arr = array('853537', '854480', '878397', '898057', '945540', '995636', '123456');
    $date_arr = array('10-01-2018', '10-03-2018', '09-24-2018', '09-28-2018', '09-30-2018', '10-03-2018');
    $start_time_arr = array('07:00:00', '19:00:00', '15:00:00', '23:00:00');

    $num_tests = 5;
    $i = 0;

    # test schedule:
    while ($i < $num_tests) {
        $i = $i + 1;
        echo '<h3 style="margin-left: 20%">Test  ' . $i . ':</h3><br><br>';

        echo '<h4 style="margin-left: 25%">Schedule Case ' . $i . ':</h4><br><br>';

        $dept = $dept_arr[array_rand($dept_arr, 1)];
        $date = $date_arr[array_rand($date_arr, 1)];
        $empid = $empid_arr[array_rand($empid_arr, 1)];
        $start_time = $start_time_arr[array_rand($start_time_arr, 1)];

        echo '<center>Department: '.$dept.'<br><br>Date: '.$date.'<br><br>EmployeeID: '.$empid.'<br><br>StartTime: '.$start_time.'<br><br></center>';

        schedule($con, $dept, $date, $empid, $start_time);

        echo '<br><br><br><h4 style="margin-left: 25%">Unschedule Case ' . $i . ':</h4><br><br>';

        $dept = $dept_arr[array_rand($dept_arr, 1)];
        $date = $date_arr[array_rand($date_arr, 1)];
        $empid = $empid_arr[array_rand($empid_arr, 1)];

        echo '<center>Department: '.$dept.'<br><br>Date: '.$date.'<br><br>EmployeeID: '.$empid.'<br><br>StartTime: '.$start_time.'<br><br></center>';

        unschedule($con, $dept, $date, $empid);


    }
}

test_cases($con);



