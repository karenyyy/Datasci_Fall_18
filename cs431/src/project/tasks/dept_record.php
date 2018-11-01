<?php
/**
 * Created by PhpStorm.
 * User: karen
 * Date: 10/24/18
 * Time: 6:00 PM
 */



require_once('../connect/connect.php');
require_once('../helper/schedulehelper.php');

function department_need($con)
{
    if (isset($_POST["department"], $_POST['emptype'], $_POST['date1'], $_POST["date2"])) {
        $dept = $_POST["department"];
        $emptype = $_POST["emptype"];
        $date1 = convert_date_format($_POST["date1"]);
        $date2 = convert_date_format($_POST["date2"]);
        $query = "SELECT s.dept AS Department,
                       s.empid AS EmployeeID,
                       s.date AS Date,
                       date_format(s.start_time, '%I%p') AS ShiftStartTime,
                       e.emptype AS EmployeeType
                FROM schedule as s, department as d, employees as e
                WHERE s.dept=d.department_name
                      AND s.empid = e.empid
                      AND s.date >= '$date1'
                      AND s.date <= '$date2'
                      AND s.dept = '$dept'
                      AND e.emptype = '$emptype'
                ORDER BY d.department_id, s.date";

        if (!($result = mysqli_query($con, $query))) {
            $msg = 'MySQL error #' . mysqli_connect_errno() . ": " . mysqli_connect_error();

            printf($msg, __FILE__, __LINE__);

        } else if (0 == mysqli_num_rows($result)) {
            echo "<center><h3>The $dept department does not need $emptype type of employee on schedule from $date1 to $date2!</h3></center><br>";
            return "";
        } else {
            echo "<br><br>";
            echo "<center><h4>The schedule list of department $dept of employee type $emptype from $date1 to $date2:</h4><br><br>";
            echo "<table class='table table-striped' border=1>";
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


department_need($con);
