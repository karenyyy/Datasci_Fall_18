<?php require_once('../helper/schedulehelper.php'); ?>

<?php require_once('navbar.php') ?>

<meta name="viewport" content="width=device-width, height=device-height, initial-scale=1.0">

<div style="margin-top: 3%">
    <h2>
        <center>First check whether the employee is available</center>
        <br>
    </h2>

    <form class="post_form" action="" method="post">

        EmployeeID : <input type="text" name="empid"><br><br>
        Schedule Date : <input type="text" name="schedule_date"> (format: 'mm-dd-yy')<br><br>

        <input class="check_button" type="submit" value="Check">

    </form>
</div>


<?php require_once('../tasks/schedule.php'); ?>
