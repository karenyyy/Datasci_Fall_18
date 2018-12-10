<?php


require_once(__DIR__.'/../../config/connect.php');
require_once(__DIR__.'/../../util/draw_report.php');


function create_unfilled_needs_report()
{
    global $db;
    $query = "
       select dept, date, shiftchar,
       if(length(emptype)>0, emptype, 'NA') as emptype,
       emp_need as unfilled_need
        from need
        where emp_need>0
        ";
    draw_report_table($query, 'Unfilled Needs');


    ###################################################################
    ######################## Total Unfilled needs #####################
    ###################################################################

    $query_for_unfilled_needs = 'select sum(unfilled_need) as total_unfilled_need from ('.$query.' ) tmp';
    $result_set = mysqli_query($db, $query_for_unfilled_needs);
    $result = mysqli_fetch_array($result_set);
    $total_unfilled_need = $result['total_unfilled_need'];
    echo '<h3>Total Unfilled Need: '.$total_unfilled_need.'</h3><br>';
}

