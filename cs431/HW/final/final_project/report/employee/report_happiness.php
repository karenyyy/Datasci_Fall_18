<?php


require_once(__DIR__.'/../../config/connect.php');
require_once(__DIR__.'/../../util/draw_report.php');


function create_happiness_report()
{
    $query = "
        select e2.empid,
                     if(tmp2.satisfied_shift_count, tmp2.satisfied_shift_count, 0) as satisfied_shift_count,
                     if(tmp2.total_shift_count, tmp2.total_shift_count, 0) as total_shift_count,
                     if(tmp2.happiness, concat(round(tmp2.happiness*100, 2),'%'), concat(50,'%')) as happiness
        from employee e2
            left join (select empid,
                              sum(satisfied_count) as satisfied_shift_count,
                              count(*) as total_shift_count,
                              sum(satisfied_count) / count(*) as happiness
                        from
                            (select s.empid, s.start_time, e.pre_shift_start, if(s.start_time=e.pre_shift_start,1,0) as satisfied_count
                             from schedule s
                             inner join employee e
                             on s.empid=e.empid) as tmp
                             group by empid) as tmp2
            on e2.empid=tmp2.empid
 ";
    draw_report_table($query, 'Happiness');
}

