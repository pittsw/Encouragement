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
            var client_id = link.id;
            $(".message-list").load("/fragment/message/" + client_id + "/");
            $(".client-profile").load("/detail/" + client_id + "/", function() {
                loadEditHandlers(link);
            });
            $(link).css("background-color", "rgb(91,141,147)");
            $(link).css("color", "rgb(217,233,236)");
            $('.name_bar').html($(link).find('.name').html());
        }
        $(".person").on("click", function(e) {
            load(this);
        });

        // Set up the asynchronous search
        var people = $('.person');
        var timer = undefined;
        var processor = undefined;
        function filter() {
            if (processor) {
                clearInterval(processor);
            }
            var busy = false, i = 0, step=10;
            var name = $.trim($('#searchtext').val()).toLowerCase();
            processor = setInterval(function() {
                if (!busy) {
                    busy = true;
                    var divs = people.slice(i, i + step);
                    divs.each(function (num) {
                        $(this).show();
                        var e = $(this);
                        var x = e.find('.name').html().toLowerCase();
                        if (x.indexOf(name) < 0) {
                            e.hide();
                        }
                    });
                    i += step;
                    if (i >= people.length) {
                        clearInterval(processor);
                    }
                    busy = false;
                }
            }, 1);
        }
        $('#searchtext').on('keyup', function(e) {
            var code = (e.keyCode ? e.keyCode : e.which);
            if (code == 27) {
                // Clear on escape
                $('#searchtext').val('');
            }
            filter();
        });

        // Load the client editing fragment when they click edit
        var loadEditHandlers = function(link) {
            var client_id = link.id;
            $('.info #edit').on("click", function(eventObject) {
                $('.view_buttons').hide();
                $('.edit_buttons').show();
                $('#client_fragment').load("/edit/" + client_id + "/", function() {
                    setCalendars();
                });
                return false;
            });

            // Save the client when they click save
            $('.info #save').on("click", function(eventObject) {
                var xhr = new XMLHttpRequest();
                xhr.open("POST", "/edit/" + client_id + "/", false);
                xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                xhr.send($('#edit_client').serialize());
                var response = xhr.responseText;
                if (response.length == 0) {
                    $('#client_fragment').load("/fragment/" + client_id + "/");
                    $('.edit_buttons').hide();
                    $('.view_buttons').show();
                } else {
                    $('#client_fragment').html(response);
                }
                return false;
            });

            // Return when they click cancel
            $('.info #cancel').on("click", function(eventObject) {
                $('#client_fragment').load('/fragment/' + client_id + '/');
                $('.edit_buttons').hide();
                $('.view_buttons').show();
                return false;
            });

            //toggle the componenet with class msg_body
            $(".info .msg_head").click(function() {
                $(this).next(".msg_body").slideToggle(600);
                if ($(this).hasClass('info_expanded')) {
                    $(this).addClass('info_collapsed').removeClass('info_expanded');
                } else {
                    $(this).addClass('info_expanded').removeClass('info_collapsed');
                }
            });

            // Hook in note saving
            $('.info .add_note').on("click", function(eventObject) {
                var xhr = new XMLHttpRequest();
                xhr.onreadystatechange = function() {
                    load(link);
                }
                xhr.open("POST", "/note/" + client_id + "/", true);
                xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                xhr.send($('#add_note_form').serialize());
            });
        };
    });
})(jQuery);

function switch_tabs(obj) {
    $('.tab-content').hide();
    $('.tabs a').removeClass("selected");
    var id = obj.attr("rel");
 
    $('#'+id).show();
    obj.addClass("selected");
}
