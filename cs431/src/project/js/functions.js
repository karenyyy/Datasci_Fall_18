
function unschedule(ScheduleID) {
    var prompt = confirm("Are you sure you want to delete this schedule?");

    if(prompt == true) {

        $.post("../tasks/delete_schedule.php", { ScheduleID: ScheduleID })
            .done(function(error) {

                if(error != "") {
                    alert(error);
                    return;
                }

            });
        location.reload();
    }
}