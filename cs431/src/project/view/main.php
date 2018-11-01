<head>
    <meta name="viewport" content="width=device-width, height=device-height, initial-scale=1.0">
    <h1>
        <center> CMPSC 431 Project simple demo</center>
    </h1>
    <h2>
        <center>jxy225</center>
    </h2>
    <br><br>
</head>


<?php

require_once('navbar.php') ;
require_once('../connect/connect.php');

function showTables($con)
{
    $query = "SHOW TABLES";
    $result = mysqli_query($con, $query);

    echo "<div style='margin-left: 30%; margin-right: auto'><h3>Show Tables:</h3></div>";

    while ($row = mysqli_fetch_assoc($result)) {
        foreach ($row as $table) {
            echo "<center><h4>$table</h4></center>";
            describeTable($con, $table);
            echo "<br>";
        }
    }
}


function describeTable($con, $table)
{
    $query = "DESCRIBE $table";
    $result = mysqli_query($con, $query);

    echo "<table class='table table-striped' style='text-align: center' border=1>";

    while($row = mysqli_fetch_array($result)) {
        echo "<tr>\n";
        echo "<td>{$row['Field']} - {$row['Type']}</td>";
        echo "</tr>\n";
    }
    echo "</table>";
}



showTables($con);
