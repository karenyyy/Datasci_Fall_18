<?php
/**
 * Created by PhpStorm.
 * User: karen
 * Date: 10/12/18
 * Time: 7:58 PM
 */

  require_once('config.php');

  function connect_to_db()
  {

      $connection = mysqli_connect(DB_MAIN_HOST, DB_MAIN_USER, DB_MAIN_PASS, DB_MAIN_NAME);

      if (mysqli_connect_errno()) {
          $msg = "Database connection failed: ";
          $msg .= mysqli_connect_error();
          $msg .= " (" . mysqli_connect_errno() . ")";
          printf($msg);
      }
      return $connection;
  }

  function close_from_db($connection)
  {
      if (isset($connection)) {
          mysqli_close($connection);
      }
  }


  function confirm_result_set($result_set)
  {
      if (!$result_set) {
          exit("Database query failed.");
      }
  }


$con = connect_to_db();
