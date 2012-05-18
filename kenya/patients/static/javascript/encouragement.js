(function($) {
    $(document).ready(function() {

        // Sets up the characters left view.
        $('#message-box').bind('keyup', function(e) {
            var len = $('#message-box').val().length;
            var messages = Math.ceil(len / 144);
            var left = len % 144;
            if (left == 0 && messages > 0) {
                left = 144;
            }
            var str = left + "/144 characters, " + messages + " message";
            if (messages != 1) {
                str += "s";
            }
            $('#chars-left').text(str);
        });

        // Sets up tab switching for the message boxes
        $('.tabs a').click(function(){
            switch_tabs($(this));
        });
        switch_tabs($('.defaulttab'));

        // Adds a date picker to every field marked as being a date
        var setCalendars = function() {
            $(".date input").each(function(index, element) {
                $(this).datepicker({
                    changeMonth: true,
                    changeYear: true,
                    dateFormat: "yy-mm-dd",
                    maxDate: "+2y",
                    minDate: "-100y",
                    selectOtherMonths: true,
                    showOtherMonths: true,
                    showOn: "button",
                    yearRange: "-100:+2"
                });
            });
        }

        // Create the add client dialog
        $("#signup").dialog({
            autoOpen: false,
            modal: true,
            width: 'auto',
            buttons: {
                "Ok": function() {
                    var xhr = new XMLHttpRequest();
                    xhr.open("POST", "/add/", false);
                    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                    xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                    xhr.send($("#add_client_form").serialize());
                    var response = xhr.responseText;
                    if (response.length == 0) {
                        window.location.href = "/";
                    } else {
                        $("#add_client_form").html(response);
                        setCalendars();
                    }
                }
            },
            open: function(event, ui) {
                setCalendars();
            },
            close: function(event, ui) {
                $("#add_client_form").load("/add/");
            }
        });
        $("#add").on("click", function() {
            $("#signup").dialog("open");
        });

        // Set up our handlers for client clicks
        var resetColors = function() {
            $(".person").css("background-color", "rgb(217, 233, 236)");
            $(".person").css("color", "rgb(0, 0, 0)");
        }
        var load = function(link) {
            resetColors();
            var id = link.id;
            $(".message-list").load("/fragment/message/messages/" + id + "/");
            $(".client-profile").load("/detail/" + id + "/");
            $(link).css("background-color", "rgb(91,141,147)");
            $(link).css("color", "rgb(217,233,236)");
        }
        $(".person").on("click", function(e) {
            load(this);
        });
    });
})(jQuery);

function switch_tabs(obj) {
    $('.tab-content').hide();
    $('.tabs a').removeClass("selected");
    var id = obj.attr("rel");
 
    $('#'+id).show();
    obj.addClass("selected");
}
