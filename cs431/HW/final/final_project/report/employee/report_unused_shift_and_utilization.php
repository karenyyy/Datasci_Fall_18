<?php

require_once(__DIR__.'/../../config/connect.php');
require_once(__DIR__.'/../../util/draw_report.php');


function create_unused_shift_and_utilization_report()
{
    $query = "
    select tmp2.empid, tmp2.firstName, tmp2.lastName, tmp2.ftpt,
       tmp2.default_shift, tmp2.total_shift_count,
       tmp2.default_shift - tmp2.total_shift_count as unused_shift_count,
       concat(round((tmp2.total_shift_count/tmp2.default_shift)*100, 2), '%') as utilization
    from
         (select e2.empid, e2.ftpt, e2.firstName, e2.lastName,
                 if(e2.ftpt='FT', 10-e2.daysoff, 6-e2.daysoff) as default_shift,
                 if(tmp.total_shift_count, tmp.total_shift_count, 0) as total_shift_count
          from (select e.empid, e.ftpt, e.firstName, e.lastName,
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
  ";


    ###################################################################
    ############## Draw Report for Unused Shift for FT ################
    ###################################################################

    $query_ft = $query.sprintf(" where ftpt=%s", "'FT'");
    draw_report_table($query_ft, 'Unused Shifts and Utilization for FT');

    ###################################################################
    ############## Draw Report for Unused Shift for PT ################
    ###################################################################

    $query_pt = $query.sprintf(" where ftpt=%s", "'PT'");
    draw_report_table($query_pt, 'Unused Shifts and Utilization for PT');
}