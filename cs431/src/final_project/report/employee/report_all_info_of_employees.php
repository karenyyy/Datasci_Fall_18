<?php

require_once(__DIR__.'/../../config/connect.php');
require_once(__DIR__.'/../../util/draw_report.php');


function create_all_report()
{
    global $db;
    $query = "
        select tmp2.empid, tmp2.firstName, tmp2.lastName, tmp2.ftpt,
               round(tmp2.total_shift_count*8*tmp2.wage, 2) as salary_cost,
               tmp2.default_shift, tmp2.total_shift_count,
               tmp2.default_shift - tmp2.total_shift_count as unused_shift_count,
               happiness_table.satisfied_shift_count as satisfied_shift_count,
               round(happiness_table.happiness, 2) as happiness,
               round((tmp2.total_shift_count/tmp2.default_shift), 2) as utilization
        from
             (select e2.empid, e2.ftpt, e2.firstName, e2.lastName, e2.wage,
                     if(e2.ftpt='FT', 10-e2.daysoff, 6-e2.daysoff) as default_shift,
                     if(tmp.total_shift_count, tmp.total_shift_count, 0) as total_shift_count
              from (select e.empid, e.ftpt, e.firstName, e.lastName, e.wage,
                           if(d.daysoff, d.daysoff, 0) as daysoff
                    from employee e
                           left join
                             (select empid, count(*) as daysoff
                              from day_off group by empid) d
                             on e.empid=d.empid) e2
                     left join
                       (select empid, count(*) as total_shift_count
                        from schedule
                        group by empid) as tmp
                       on e2.empid=tmp.empid) as tmp2
        inner join (
                   select empid,
                          sum(satisfied_count) as satisfied_shift_count,
                          sum(satisfied_count) / count(*) as happiness
                   from
                        (select s.empid, s.start_time, e.pre_shift_start,
                                if(s.start_time=e.pre_shift_start,1,0) as satisfied_count
                         from schedule s
                                inner join employee e
                                  on s.empid=e.empid) as tmp
                   group by empid
                 ) happiness_table
        on tmp2.empid=happiness_table.empid
 ";

    $query_all = 'SELECT 
                        empid as EmployeeID, 
                        firstName as FirstName, 
                        lastName as LastName, 
                        ftpt as `FT/PT`,
                        concat(\'$\', salary_cost) as Cost,
                        default_shift as `Default Shift`, 
                        total_shift_count as `Total Shift Count`,
                        unused_shift_count as `Unused Shift Count`,
                        satisfied_shift_count as `Satisfied Shift Count`,
                        concat(happiness*100, \'%\') as Happiness,
                        concat(utilization*100, \'%\') as Utilization
                  FROM ('.$query.') as table_final';

    draw_report_table($query_all, 'Employee');


    ###################################################################
    ####################### Calculate Total Cost ######################
    ###################################################################

    $query_for_cost = 'SELECT sum(salary_cost) as total_cost FROM ('.$query.') as table_cost';
    $result_set = mysqli_query($db, $query_for_cost);
    $result = mysqli_fetch_array($result_set);
    echo '<h3>Total Cost: $'.$result['total_cost'].'</h3>';


    ###################################################################
    ##################### Calculate Average Happiness #################
    ###################################################################

    $query_for_happiness = 'SELECT round(avg(happiness), 4) as avg_happiness FROM ('.$query.') as table_happiness';
    $result_set = mysqli_query($db, $query_for_happiness);
    $result = mysqli_fetch_array($result_set);
    $avg_happiness = $result['avg_happiness']*100;
    echo '<h3>Average Employee Happiness: '.$avg_happiness.'%</h3>';


    ###################################################################
    ############## Calculate Total Unused Shifts for FT ###############
    ###################################################################

    $query_for_unused_shift_ft = 'select sum(unused_shift_count) as total_unused_shift_count
                                  from ('.$query.' ) table_unused_shift where ftpt=\'FT\'';
    $result_set = mysqli_query($db, $query_for_unused_shift_ft);
    $result = mysqli_fetch_array($result_set);
    $total_unused_shift_ft = $result['total_unused_shift_count'];
    echo '<h3>Total Unused Shifts for Full Time Employee: '.$total_unused_shift_ft.'</h3>';


    ###################################################################
    ############## Calculate Total Unused Shifts for PT ###############
    ###################################################################

    $query_for_unused_shift_pt = 'select sum(unused_shift_count) as total_unused_shift_count
                                  from ('.$query.' ) table_unused_shift where ftpt=\'PT\'';
    $result_set = mysqli_query($db, $query_for_unused_shift_pt);
    $result = mysqli_fetch_array($result_set);
    $total_unused_shift_pt = $result['total_unused_shift_count'];
    echo '<h3>Total Unused Shifts for Part Time Employee: '.$total_unused_shift_pt.'</h3>';


    ###################################################################
    ############## Calculate Average utilization for FT ###############
    ###################################################################

    $query_for_utilization_ft = 'SELECT round(avg(utilization),4) as avg_utilization_ft FROM ('.$query.' where tmp2.ftpt=\'FT\') as table_utilization1';
    $result_set = mysqli_query($db, $query_for_utilization_ft);
    $result = mysqli_fetch_array($result_set);
    $avg_utilization_ft = $result['avg_utilization_ft']*100;
    echo '<h3>Average Full-Time Employee Utilization: '.$avg_utilization_ft.'%</h3>';

    ###################################################################
    ############## Calculate Average utilization for PT ###############
    ###################################################################

    $query_for_utilization_pt = 'SELECT round(avg(utilization),4) as avg_utilization_pt FROM ('.$query.' where tmp2.ftpt=\'PT\') as table_utilization2';
    $result_set = mysqli_query($db, $query_for_utilization_pt);
    $result = mysqli_fetch_array($result_set);
    $avg_utilization_pt = $result['avg_utilization_pt']*100;
    echo '<h3>Average Part-Time Employee Utilization: '.$avg_utilization_pt.'%</h3>';

    echo '<br>';

}

