<?php require_once('navbar.php') ?>
<?php require_once('../helper/schedulehelper.php'); ?>

    <meta name="viewport" content="width=device-width, height=device-height, initial-scale=1.0">

    <div style="margin-top: 3%">
        <h2>
            <center> See the schedule need of each department</center>
        </h2>
        <br>

        <form class="post_form" action="" method="post">
            <br>
            Department:
            <select name="department">
                <?php echo departmentList($con) ?>
            </select><br><br>

            Employee Type:
            <select name="emptype">
                <option value="RN"> RN</option>
                <option value="LPN"> LPN</option>
            </select><br><br>

            From Date: <input type="text" name="date1"> (format: 'mm-dd-yy')<br><br>
            To Date: <input type="text" name="date2"> (format: 'mm-dd-yy')<br><br>
            <input class="check_button" type="submit" value="Check">

        </form>
        <br><br>
    </div>

<?php require_once('../tasks/dept_record.php'); ?>