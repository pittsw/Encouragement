(function($) {
    $(document).ready(function() {

        // The id of the currently selected client
        var client_id = undefined;

        // The name of the currently selected client
        var client_name = undefined;

        // The load timer that automatically refreshed the page
        var load_timer = undefined;

        // Set up AJAX to allow posts
        $.ajaxSetup({ 
             beforeSend: function(xhr, settings) {
                 function getCookie(name) {
                     var cookieValue = null;
                     if (document.cookie && document.cookie != '') {
                         var cookies = document.cookie.split(';');
                         for (var i = 0; i < cookies.length; i++) {
                             var cookie = jQuery.trim(cookies[i]);
                             // Does this cookie string begin with the name we want?
                         if (cookie.substring(0, name.length + 1) == (name + '=')) {
                             cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                             break;
                         }
                     }
                 }
                 return cookieValue;
                 }
                 if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                     // Only send the token to relative URLs i.e. locally.
                     xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                 }
             } 
        });
        
        //Load Client View Into Main Content
        var load_client = function(client_obj) {
			var fragment_url = "/fragment/display_client/?";
			if(client_obj){
				fragment_url += "id="+client_obj.id;
			}
			if($("#select_msg") && $("#select_msg").val() == "list") {
				if (fragment_url.length > 26) { //second get vaiable
					fragment_url += "&";
				}
				fragment_url += "list=1";
			}
			$('#main_content').load(fragment_url,function() {load_client_complete(client_obj)})
		}
		
		var load_client_complete = function(client_obj) {
			
			load_message_call_tabs();
			
			if(client_obj) {
				client_id = client_obj.id;
				client_name = $(client_obj).find('.name').html();
			}
			
			 // Change message displays when the user selects the pulldown
			$('.message_bar .download').html('<a href="/msgcsv/' + client_id + '/">Download</a>');
			$("#select_msg").on("change", function(e) {
				if($("#select_msg").val() == "list") {
					$(".message-list").load("/fragment/message_list/" + client_obj.id + "/");
				} else {
					$(".message-list").load("/fragment/message/" + client_obj.id + "/");
				}
			});
            
			loadEditHandlers(client_obj);
        }
        
        var load_message_call_tabs = function () {
			 // Swap the boxes in add call when the call completed button is changed
			$('#complete').on('change', function(e) {
				if (this.checked) {
					$('.duration').show();
				} else {
					$('#duration').val('');
					$('.duration').hide();			
				}
			});
			$('.duration').hide();

			$('#clear_call').on('click', function(e) {
				$('#call_notes').val("");
				$('#duration').val('');
				$('#complete').attr('checked', false);
				$('.duration').hide();
			});
			
			// Sets up the characters left view.
			$('#message-box').on('keyup', function(e) {
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
            
            // Send a message when the nurse clicks send
        
			$('.messages #send_message').on("mouseleave", function() {
				$("#send_message").css("background-color", "rgb(91,141,147)");
			});
			
			$('.messages #send_message').on("mousedown", function() {
				$("#send_message").css("background-color", "rgb(217, 233, 236)");
				}).on('mouseup', function() {
				$("#send_message").css("background-color", "rgb(91,141,147)");
				if (client_id === undefined || $(".messages #message-box").val() == "") {
					return;
				}
				var xhr = new XMLHttpRequest();
				xhr.onreadystatechange = function() {
					if (xhr.readyState != 4) {
						return;
					}
					if($("#select_msg").val() == "list") {
						$(".message-list").load("/fragment/message_list/" + client_id + "/");
					} else {
						$(".message-list").load("/fragment/message/" + client_id + "/");
					}
					$(".messages #message-box").val("").keyup();
				}
				xhr.open("POST", "/message/" + client_id + "/", true);
				xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
				xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
				xhr.send($('#message-box').serialize());
			});

			// Save a call when the nurse clicks save
			 $('.messages #save_call').on("mouseleave", function() {
				$("#save_call").css("background-color", "rgb(91,141,147)");
			});
			
			$('.messages #save_call').on("mousedown", function() {
				$("#save_call").css("background-color", "rgb(217, 233, 236)");
				}).on('mouseup', function() {
				$("#save_call").css("background-color", "rgb(91,141,147)");
				if (client_id == undefined) {
					return;
				}
				var xhr = new XMLHttpRequest();
				xhr.onreadystatechange = function() {
					if (xhr.readyState != 4) {
						return;
					}
					if($("#select_msg").val() == "list") {
						$(".message-list").load("/fragment/message_list/" + client_id + "/");
					} else {
						$(".message-list").load("/fragment/message/" + client_id + "/");
					}
					$('#call_notes').val("");
					$('#duration').val('');
					$('#complete').attr('checked', false);
					$('.duration').hide();
				}
				xhr.open("POST", "/add_call/" + client_id + "/", true);
				xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
				xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
				xhr.send($('#phone-box').serialize());
			});
			
			create_tabs($('.messages #tabs'));
		}
        
        var load_add_client = function() {
			$('#main_content').load("/add", function() {load_add_client_complete()});
		}
		
		var load_add_client_complete = function() {
			setCalendars();
			//randomize day
			$("#id_message_day").val(Math.floor(Math.random()*7));
			$("#add_client_form #submit").on("click", function () {
				var xhr = new XMLHttpRequest();
				xhr.open("POST", "/add/", false);
				xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
				xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
				var data = $("#add_client_form").serialize()
				data = data.slice(0,data.lastIndexOf("csrfmiddle")); //HACK: serialize was doubling the form!
				xhr.send(data);
				var response = xhr.responseText;
				if (/^\d+$/.test(response)) { // a single number is the new user id
					window.location = "/?id="+response;
				} else {
					$("#main_content").html(response); 
					load_add_client_complete();
				}
			});
		}
		
        $("#add").on("click", function() {
            load_add_client();
        });
        
           // Switch tabs
        var switch_tabs = function(obj) {
            var tabs = $(obj.parents()[2])
            tabs.children('.tab-content').hide();
            tabs.find('.tabs a').removeClass("selected");
            var id = obj.attr("rel");
         
            $('#'+id).show();
            obj.addClass("selected");
         }

		var create_tabs = function(obj) {
			// Hook in tab switching
			obj.find('.tabs a').on('click', function(){
				switch_tabs($(this));
			});
			//Set Default Tabs
			obj.find('.defaulttab').each(function(i,ele){switch_tabs($(ele))});
		}

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
        
        var getURLParameter = function(name) {
			 return decodeURIComponent((RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
		}
		
		if(getURLParameter('id')) {
			load_client({'id':getURLParameter('id')});
		}

        // Set up the asynchronous search
        //var people = $('.person');
        //var processor = undefined;
        function filter() {
            if (processor) {
                clearInterval(processor);
            }
            var busy = false, i = 0, step=10;
            var name = $.trim($('#searchtext').val()).toLowerCase();
            var processor = setInterval(function() {
                if (!busy) {
                    busy = true;
                    var divs = people.slice(i, i + step);
                    divs.each(function (num) {
                        
                        var temp_name = $(this).find('.client_name').html().toLowerCase();
                        if (temp_name.indexOf(name) < 0) {
                            $(this).hide();
                        }
                        else {
							$(this).show();
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
        
        //Add Filter Actions
        var load_client_list = function() {
			var url = "/fragment/list/?group=";
			url+=$('#group_select').val()+"&sort="+$('#sort_select').val();
			$('#patient_list').load(url,load_client_list_complete);
		}
		$('#group_select').on('change',load_client_list);
        $('#sort_select').on('change',load_client_list);
        
       // Register click handlers on all clients
        var load_client_list_complete = function() {
            $(".person").on("click", function() {
               //change css on selected person
               $(".person_selected").removeClass("person_selected");
               $(".list #"+this.id).addClass("person_selected");
                load_client(this);
            });
            people = $('.person');
           filter();
        }
		load_client_list_complete();
        
        // Load the client editing fragment when they click edit
        var loadEditHandlers = function(link) {
			setCalendars();
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
            $(".info .msg_head").on('click', function() {
                $(this).next(".msg_body").slideToggle(600);
                if ($(this).hasClass('info_expanded')) {
                    $(this).addClass('info_collapsed').removeClass('info_expanded');
                } else {
                    $(this).addClass('info_expanded').removeClass('info_collapsed');
                }
            }
            
            );

            // Hook in note adding
            $('.info #notes_add').on('click', function() {
                $('.info #note').show();
                $('.info #notes_hide').show();
                $(this).hide();
                return false;
            });

            // Hook in hiding the note form
            $('.info #notes_hide').on('click', function() {
                $('.info #note').hide();
                $('.info #note [name=text]').val('');
                $('.info #notes_add').show();
                $(this).hide();
                return false;
            });

            // Hook in note deleting
            $('.info #notes .delete').each(function(i, e) {
                var pk = $(this).attr('id');
                $(this).on('click', function() {
                    $.post("/delete_note/" + pk + "/", {}, function() {
                        load_client(link);
                    });
                });
            });

            // Hook in note saving
            $('.info .add_note').on("click", function(eventObject) {
                var xhr = new XMLHttpRequest();
                xhr.onreadystatechange = function() {
                    if (xhr.readyState != 4) {
                        return;
                    }
                    load_client(link);
                }
                xhr.open("POST", "/note/" + client_id + "/", true);
                xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                xhr.send($('#add_note_form').serialize());
            });

            // Hook in visit adding
            $('.info #visit_add').on("click", function(eventObject) {
				if($(this).parent().hasClass('info_collapsed')){
					toggle_msg($(this).parent())
				}
                $('.info #visit_form_container').show();
                $(this).hide();
                $('.info #visit_hide').show();
                return false;
            });

            // Hook in visit hiding
            $('.info #visit_hide').on("click", function(eventObject) {
                $('.info #visit_form_container').hide();
                $(this).hide();
                $('.info #visit_add').show();
                return false;
            });
            $('.info #visit_form_container').hide();

            // Hook in visit saving
            $('.info #add_visit').on("click", function(eventObject) {
                var xhr = new XMLHttpRequest();
                xhr.onreadystatechange = function() {
                    if (xhr.readyState != 4) {
                        return;
                    }
                    load_client(link);
                }
                xhr.open("POST", "/visit/" + client_id + "/", true);
                xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                xhr.send($('#add_visit_form').serialize());
            });

            // Hook in visit deleting
            $('.info #visits .delete').each(function(i, e) {
                var pk = $(this).attr('id');
                $(this).on('click', function() {
                    $.post("/delete_visit/" + pk + "/", {}, function() {
                        load_client(link);
                    });
                });
            });
        };
        
        var toggle_msg = function(obj) {
                $(obj).next(".msg_body").slideToggle(600);
                if ($(obj).hasClass('info_expanded')) {
                    $(obj).addClass('info_collapsed').removeClass('info_expanded');
                } else {
                    $(obj).addClass('info_expanded').removeClass('info_collapsed');
                }
            }
    });
})(jQuery);
