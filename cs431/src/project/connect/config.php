<?php
/**
 * Created by PhpStorm.
 * User: karen
 * Date: 10/12/18
 * Time: 7:58 PM
 */


$url = parse_url(getenv("CLEARDB_DATABASE_URL"));


$server = $url["host"];
$username = $url["user"];
$password = $url["pass"];
$db = substr($url["path"], 1);


//$server = 'localhost';
//$username = 'root';
//$password = 'sutur1,.95';
//$db = 'cs431_project';


define("DB_MAIN_HOST", $server);
define("DB_MAIN_USER", $username);
define("DB_MAIN_PASS", $password);
define("DB_MAIN_NAME", $db);
