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
});
