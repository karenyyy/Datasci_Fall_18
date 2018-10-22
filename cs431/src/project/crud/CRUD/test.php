<?php
/**
 * Created by PhpStorm.
 * User: karen
 * Date: 10/10/18
 * Time: 12:09 AM
 */


$DB_MAIN_HOST = "localhost";
$DB_MAIN_NAME = "cs431_project";
$DB_MAIN_USER = "root";
$DB_MAIN_PASS = "sutur1,.95";
$connection = mysqli_connect($DB_MAIN_HOST, $DB_MAIN_USER, $DB_MAIN_PASS, $DB_MAIN_NAME, 3308);


function openDatabase($connection, $DB_MAIN_HOST, $DB_MAIN_USER, $DB_MAIN_PASS, $DB_MAIN_NAME)
{
    if ($connection) {
        if (!mysqli_select_db($connection, $DB_MAIN_NAME)) {
            $msg = 'MySQL error #' . mysqli_connect_errno() . ": " . mysqli_connect_error();
            printf($msg, __FILE__, __LINE__);
        }
    } else {
        $msg = 'MySQL error #' . mysqli_connect_errno() . ": " . mysqli_connect_error();
        printf($msg, __FILE__, __LINE__);
    }
}

function closeDatabase($connection)
{
    mysqli_close($connection);
}

function executeCommand($connection, $query, $zeroOk = true)
{
    if (!($result = mysqli_query($connection, $query))) {
        $msg = 'MySQL error #' . mysqli_connect_errno() . ": " . mysqli_connect_error();
        printf($msg, __FILE__, __LINE__);
    } else if ((0 == mysqli_affected_rows($connection)) && (!$zeroOk)) {
        $msg = 'Zero rows affected by command';
        printf($msg, __FILE__, __LINE__);
    } else {
        ; // everything is ok
    }
}

function terminate($connection, $empid)
{

    $query = "UPDATE employees SET status = \"T\" WHERE empid = " . $empid;
    if (!($result = mysqli_query($connection, $query))) {
        printf("Sorry! This employee was not properly terminated.");
        return false;
    }
    printf("Successfully terminated employee %s.\n", $empid);
    return true;
}

function getData($connection)
{
    $query = "SELECT * FROM employees";
    if (!($result = mysqli_query($connection, $query))) {
        $msg = 'MySQL error #' . mysqli_connect_errno() . ": " . mysqli_connect_error();
        printf($msg, __FILE__, __LINE__);
    } else if (0 == mysqli_num_rows($result)) {
        printf("No data are available!\n");
        return "";
    } else {
        while ($row = mysqli_fetch_array($result)) {
            $lastname = $row["lastname"];
            $firstname = $row["firstname"];
            printf("%s %s\n", $lastname, $firstname);
            echo '<br>';
        }
    }
}

getData($connection);