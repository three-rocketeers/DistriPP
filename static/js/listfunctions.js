$(document).ready(function () {

    //on click
    $('#listadd').click(function () {

        var userInput = $("#new-item").val();
        console.log("User inputted...", userInput);

        if (!userInput) {
            $('.error').toggle();
            $('.error').text('Please enter a story number!').show();
        }
        else {
            $('#list-items').append("<li class='list-group-item'>" + userInput + "<i class='fa fa-trash fa-4'></i>" + "</li>");
        }

        $('#new-item').val("");

    });
    //end on click

    //remove list item on click of trash icon
    $(".list-items").on("click", ".fa-trash", function () {
        $(this).closest("li").remove();
        console.log("Removing item", $(this).closest("li"));
    });

    //remove error message on focusing the input
    $("#new-item").val('').focus(function () {
        $('.error').toggle();
    });

});