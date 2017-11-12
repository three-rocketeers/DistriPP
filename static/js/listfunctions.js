$(document).ready(function () {

    //on click
    $('#listadd').click(function () {

        var userInput = $("#new-item").val();
        console.log("User inputted...", userInput);
        /*
         //Comment back in if errors should be thrown when entering empty and comment out the following block
         if (!userInput) {
         $('.error').collapse("show");
         $('.error').text('Please enter a story number!').show();
         }
         else {
         console.log('check');
         $('#list-items').append("<li class='list-group-item'>" + userInput + "<i class='fa fa-trash fa-4'></i>" + "</li>");
         }
         */
        if (userInput) {
            $('#list-items').append('<div class="input-group"> <input type="text" class="form-control" name="stories" value="' + userInput + '" aria-label="story"> <span class="input-group-btn"> <button class="btn btn-secondary" type="button"><i class="fa fa-trash float-right" aria-hidden="true"></i></button> </span> </div>');
            //$('#list-items').append("<li class='list-group-item'><input class='no-border' type='text' name='stories' readonly value='" + userInput + "'><i class='fa fa-trash float-right' aria-hidden='true'></i>" + "</li>");
        }

        $('#new-item').val("");

    });
    //end on click

    //remove list item on click of trash icon
    $("#list-items").on("click", ".fa-trash", function () {
        $(this).closest("li").remove();
        console.log("Removing item", $(this).closest("li"));
    });

    /*
     //Comment back in if errors should be thrown when entering empty
     //remove error message on focusing the input
     $("#new-item").val('').focus(function () {
     $('.error').collapse("hide");
     });
     */
});