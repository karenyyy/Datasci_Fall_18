<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<script src="../js/functions.js"></script>


<?php
/**
 * Created by PhpStorm.
 * User: karen
 * Date: 10/12/18
 * Time: 8:03 PM
 */


require_once('../connect/connect.php');
require_once('../helper/schedulehelper.php');


function schedule_employees($con)
{
    if (isset($_POST["empid"], $_POST['schedule_date'])) {
        $empid = $_POST["empid"];
        $schedule_date = convert_date_format($_POST["schedule_date"]);

        $query = "SELECT firstname, lastname
                  FROM employees
                  WHERE empid = '$empid'";
        $result = mysqli_query($con, $query);

        if (0 == mysqli_num_rows($result)) {
            echo '<br><br>
                    <h3 style="color: red"><center>No Employee <i>' . $empid . '</i> in the database! Please double check!</center></h3>';
        } else {
            $row = mysqli_fetch_assoc($result);
            $firstname = $row['firstname'];
            $lastname = $row['lastname'];

            $query = "SELECT *
                FROM schedule
                WHERE empid='$empid'
                AND date='$schedule_date'";

            $result = mysqli_query($con, $query);

            if (!($result)) {
                $msg = 'MySQL error #' . mysqli_connect_errno() . ": " . mysqli_connect_error();
                printf($msg, __FILE__, __LINE__);
            } else if (0 == mysqli_num_rows($result)) {

                echo '<br>
                    <h4><center><i>' . $firstname . ' ' . $lastname . '</i> (id: '.$empid.') is open for schedule on ' . $schedule_date . '</center></h4><br><br>';

                echo '<h2><center>Schedule <i>' . $firstname . ' ' . $lastname . '</i> (id: '.$empid.')</center></h2><br>
                    <form class="post_form" action="" method="post">
                        EmployeeID : <input type="text" name="employee_id" value="' . $empid . '"><br><br>
                        FirstName : <input type="text" name="firstname_to_schedule" value="' . $firstname . '"><br><br>
                        LastName : <input type="text" name="lastname_to_schedule" value="' . $lastname . '"><br><br>
                        Date To Schedule : <input type="text" name="date_to_schedule" value="' . $schedule_date . '"><br><br>
                        Department To Schedule:
                        <select name="dept_to_schedule">' . departmentList($con) . '</select><br><br>
                        Start Time :  <select name="start_time_to_schedule">' . startTimeList($con) . '</select><br><br>
                        <input class="check_button" type="submit" value="Go"></form><br><br>';
            } else {
                echo "<br><br>";
                echo "<h3><center><i>$firstname $lastname </i>has already been scheduled on $schedule_date:</center></h3><br><br>";
                echo "<table class='table table-striped' border=1>";
                echo "<tr>";
                $i = 0;
                while ($i < mysqli_num_fields($result)) {
                    $meta = mysqli_fetch_field_direct($result, $i);
                    echo '<td>' . $meta->name . '</td>';
                    $i = $i + 1;
                }
                echo '<td>Unschedule</td>';

                while ($row = mysqli_fetch_assoc($result)) {
                    echo "<tr>\n";
                    foreach ($row as $cell) {
                        echo "<td> $cell </td>";
                    }
                    $schedule_id = $row['schedule_id'];
                    echo '<td><button onclick="unschedule(' . $schedule_id . ')">delete</button></td>';
                    echo "</tr>\n";
                }

                echo "</table>";


            }

        }
    }
}


function chooseShiftLen($con)
{
    if (isset($_POST["employee_id"],
        $_POST["firstname_to_schedule"],
        $_POST["lastname_to_schedule"],
        $_POST["date_to_schedule"],
        $_POST["dept_to_schedule"],
        $_POST["start_time_to_schedule"]) and !isset($_POST["shiftlen_to_schedule"])) {
        $empid = $_POST["employee_id"];
        $firstname = $_POST["firstname_to_schedule"];
        $lastname = $_POST["lastname_to_schedule"];
        $date_to_schedule = $_POST["date_to_schedule"];
        $schedule_start_time = $_POST["start_time_to_schedule"];


        echo '<br><br><h3><center>Choose shift length for <i>' . $firstname . ' ' . $lastname . '</i></center></h3><br>
                    <form class="post_form" action="" method="post">
                        EmployeeID : <input type="text" name="employee_id" value="' . $empid . '"><br><br>
                        FirstName : <input type="text" name="firstname_to_schedule" value="' . $firstname . '"><br><br>
                        LastName : <input type="text" name="lastname_to_schedule" value="' . $lastname . '"><br><br>
                        Date To Schedule : <input type="text" name="date_to_schedule" value="' . $date_to_schedule . '"><br><br>
                        Department To Schedule:
                        <select name="dept_to_schedule">' . departmentList($con) . '</select><br><br>
                        Start Time : <input type="text" name="start_time_to_schedule" value="' . $schedule_start_time . '"><br><br>
                        Shift Length : <select name="shiftlen_to_schedule">' . shiftlenList($con, $schedule_start_time) . '</select><br><br>
                        <input class="check_button" type="submit" value="schedule"></form><br><br>';

    }
}


function insert($con)
{
    if (isset($_POST["employee_id"],
        $_POST["firstname_to_schedule"],
        $_POST["lastname_to_schedule"],
        $_POST["date_to_schedule"],
        $_POST["dept_to_schedule"],
        $_POST["start_time_to_schedule"],
        $_POST["shiftlen_to_schedule"])) {
        $empid = $_POST["employee_id"];
        $firstname = $_POST["firstname_to_schedule"];
        $lastname = $_POST["lastname_to_schedule"];
        $date_to_schedule = $_POST["date_to_schedule"];
        $dept_to_schedule = $_POST["dept_to_schedule"];
        $schedule_start_time = $_POST["start_time_to_schedule"];
        $shift_len = $_POST["shiftlen_to_schedule"];


        $query = "INSERT INTO schedule (date, empid, dept, start_time, shift_length) VALUES
                      ('$date_to_schedule',
                       '$empid',
                       '$dept_to_schedule',
                       '$schedule_start_time',
                        $shift_len)";

        if (!($result = mysqli_query($con, $query))) {
            $msg = 'MySQL error #' . mysqli_connect_errno() . ": " . mysqli_connect_error();
            printf($msg, __FILE__, __LINE__);
        } else {
            echo '<br><br><h2><center>Schedule <i>' . $firstname . ' ' . $lastname . '</i> (id: '.$empid.')</center></h2><br>
                    <form class="post_form" action="" method="post">
                        EmployeeID : <input type="text" name="employee_id" value="' . $empid . '"><br><br>
                        FirstName : <input type="text" name="firstname_to_schedule" value="' . $firstname . '"><br><br>
                        LastName : <input type="text" name="lastname_to_schedule" value="' . $lastname . '"><br><br>
                        Date To Schedule : <input type="text" name="date_to_schedule" value="' . $date_to_schedule . '"><br><br>
                        Department To Schedule:
                        <select name="dept_to_schedule">' . departmentList($con) . '</select><br><br>
                        Start Time : <input type="text" name="start_time_to_schedule" value="' . $schedule_start_time . '"> <br><br>
                        Shift Length : <select name="shiftlen_to_schedule">' . shiftlenList($con, $schedule_start_time) . '</select><br><br>
                        <input class="check_button" type="submit" value="schedule"></form><br><br>';

            echo '<h3 style="color: darkgreen"><center>Employee <i>' . $firstname . ' ' . $lastname . '</i> 
                    is scheduled on ' . $date_to_schedule . ' starting from ' . $schedule_start_time . ' for
                     ' . $shift_len . ' hours in ' . $dept_to_schedule . '</center></h3><br><br>';


        }
    }
}




schedule_employees($con);
chooseShiftLen($con);
insert($con);
































