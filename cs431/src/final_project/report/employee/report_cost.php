<?php

require_once(__DIR__.'/../../config/connect.php');

//Total schedule cost
function cal_total_cost(){
    global $db;
    $query = "
        SELECT SUM(8*b.wage) AS cost 
        FROM schedule a, employee b 
        WHERE a.empid = b.empid";
    $result_cost = mysqli_fetch_assoc(mysqli_query($db, $query));
    echo "<br />" . "Total schedule cost is $" . $result_cost['cost'] . "<br />";
}
