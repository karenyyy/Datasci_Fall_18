<?php

require_once(__DIR__.'/../config/connect.php');


function draw_report_table($query, $reportname){
    global $db;
    $result = mysqli_query($db, $query);
    echo "<center><h2>".$reportname." Report</h2></center>";
    echo "<br><table class='table table-striped' border=1>";
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


