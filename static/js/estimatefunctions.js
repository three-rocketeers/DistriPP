$(document).ready(function () {
    $(".estimatebox").change(function () {
        var value = this.value;
        var id = "#" + this.id;
        $(id + "_cell").html(value);
    });

    $(".commentbox").focusout(function () {
        var value = this.value;
        var id = "#" + this.id;
        $(id + "_cell").html(value);
    });
    $('#submit_estimates').on('click', function () {
        var global_data = $('#global-data').data();
        var result_list = [];
        $('#estimates_table > tbody > tr').each(function () {
            $this = $(this);
            var data = $this.find('td');
            var storyid = data[0].innerHTML;
            var storyname = data[1].innerHTML;
            var estimate = data[2].innerHTML;
            var comment = data[3].innerHTML;
            result_list.push({storyid: storyid, storyname: storyname, estimate: estimate, comment: comment});
        });
        var json_data = JSON.stringify({data: result_list, user: global_data.username});
        $.ajax({
            url: '/save',
            data: json_data,
            contentType: 'application/json;charset=UTF-8',
            type: 'POST',
            success: function (response) {
                window.location= "/saved?planning=" + global_data.planning
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});
