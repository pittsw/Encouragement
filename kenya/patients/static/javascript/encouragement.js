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
			$('#main_content').load(fragment_url,function() {load_client_complete(client_obj)});
		}
		
		var load_client_complete = function(client_obj) {
			
			load_message_call_tabs();
			if(client_obj) {
				client_id = client_obj.id;
				client_name = $(client_obj).find('.name').html();
			}
			
			 // Change message displays when the user selects the pulldown
			$('.message_bar .download').html('<a href="/msgcsv/' + client_id + '/">Download</a>');
			$("#select_msg").on("change", load_message_fragment);
            load_message_fragment();
			loadEditHandlers(client_obj);
			var now = new Date();
			$('#time').html(now.getHours()+":"+now.getMinutes()+":"+now.getSeconds());
			$(client_obj).find('.pending').remove();
			$(client_obj).find('.pending_msg').remove();
        }
        
        //Get the list of messages for current client
        var load_message_fragment = function () {
			$(".message-list").load("/fragment/message/" + client_id + "/?mode="+$("#select_msg").val(), function (e) {
				if ($("#select_msg").val() == "conversation") {
					$(".message-list .Client input[type='checkbox']").click(function () {
						var checked = $(this).is(':checked');
						 $.post("/message/prompted/"+$(this).attr('rel')+"/?prompted="+checked); //send post for message promted
						$(this).parent().css('font-weight',(checked)?'bold':'normal');
					});
				}
			});
		}
		
		var toggle_duration_box = function(toggle) {
			var box = $('#duration_box');
			var input = $('#duration');
			if (!toggle) {
				toggle = (box.css('display')=='none')?'show':'hide';
			}
			if(toggle=='show' || toggle==true) {
				box.css('display','inline');
				input.val('1');
			}
			else {
				box.hide();
				input.val('');
			}
		}
        
        var load_message_call_tabs = function () {
			 // Swap the boxes in add call when the call completed button is changed
			$('#complete').on('change', function(e) {
				toggle_duration_box(this.checked);
			});
			//Swap the boxes in add call when client calls
			$('input[name="initiated"]').change(function(e){
				toggle_duration_box($($('input[name="initiated"]')[1]).checked);
			});
			toggle_duration_box('hide');

			$('#clear_call').on('click', function(e) {
				$('#call_notes').val("");
				$('#complete').attr('checked', false);
				toggle_duration_box('hide');
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
          
			// Send a message when nurse clicks send
			$('.messages #send_message').on("mousedown", function() {
				$("#send_message").css("background-color", "rgb(217, 233, 236)");
			}).on('mouseup', function() {
				if (client_id === undefined || $(".messages #message-box").val() == "") {
					$("#send_message").css("background-color", "rgb(91,141,147)");
					return;
				}
				$.post("/message/" + client_id + "/",$('#message-box').serialize(),function() {
					load_message_fragment();
					$(".messages #message-box").val("").keyup();
					$("#send_message").css("background-color", "rgb(91,141,147)");
				});
			});

			// Save a call when the nurse clicks save
			$('.messages #save_call').on("mousedown", function() {
				$("#save_call").css("background-color", "rgb(217, 233, 236)");
			}).on('mouseup', function() {
				if (client_id == undefined) {
					$("#save_call").css("background-color", "rgb(91,141,147)");
					return;
				}
				if(!$('#complete').checked) {
					$('#duration').val('');
				}
				$.post("/add_call/" + client_id + "/",$('#phone-box').serialize(),function() {
					load_message_fragment();
					$("#save_call").css("background-color", "rgb(91,141,147)");
					$('#call_notes').val("");
					$('#duration').val('');
					$('#complete').attr('checked', false);
					$('#duration_box').hide();
				});
			});
			create_tabs($('.messages #tabs'));
		}
        
        //Load the add client page into main frame.
        var load_add_client = function() {
			$('#main_content').load("/add", function() {load_add_client_complete()});
		}
		
		var load_add_client_complete = function() {
			setCalendars();
			//randomize day
			$("#id_send_day").val(Math.floor(Math.random()*7));
			$("#add_client_form #submit").click(function () {
				$.post('/add/',$("#add_client_form").serialize(),function (response) {
					if (/^\d+$/.test(response)) { // a single number is the new user id
					window.location = "/?id="+response;
					} else {
						$("#main_content").html(response); 
						load_add_client_complete();
					}
				},'text');
			});
		}
		
        $("#add").on("click", function() {load_add_client();});
        //End add client setup
        
        //Load Visit History page into main frame
        var load_visit_history = function () {
			$('#main_content').load("/visit_history/", function() {load_visit_history_complete()});
		}
		
		var load_visit_history_complete = function () {
			setCalendars();
			//set up checkbox toggle
			$('#visit_history_form input[type="checkbox"]').change(function(evt) {
				var chk = $(this)
				if (chk.attr("checked")) {
					chk.next().show();			
				}else {
					chk.next().hide();
				}	
			});
			//set up form post
			$('#visit_history_form #submit').click(function() {
				$.post('/visit_history/',$('#visit_history_form').serialize(),function(response) {
					$('#main_content').html(response);
				},'text');
			});
		}
		
		$('#visit_history_button').click(function() {load_visit_history();});
        //End Visit History
        
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
                    maxDate: "+1y",
                    minDate: "-50y",
                    selectOtherMonths: true,
                    showOtherMonths: true,
                    showOn: "button",
                    yearRange: "-50:+1"
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
        var processor = null;
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
                        
                        var temp_name = $(this).find('.client_name').html().toLowerCase();
                        var temp_id = $(this).find('.client_id').html();
                        if (  temp_id.indexOf(name) >= 0 || temp_name.indexOf(name) >= 0) {
                            $(this).show();
                        }
                        else {
							$(this).hide();
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
			//set date class on end pregnacy form (easy here then in django code)
			$("#end_pregnacy_form #id_end-date").parent().addClass("date");
			setCalendars();
            $('.info #client_info_edit').on("click", function(eventObject) {
                $('#client_info_edit').hide();
                $('#client_info_hide').show();
                $('#client_fragment').load("/edit/" + client_id + "/", function client_edit_callback() {
                    setCalendars();
                    // Save the client when they click save
                    $('#client_info_save').on('click', function(e) {
						$.post("/edit/"+client_id+"/",$('#edit_client').serialize(), function(data) {
							if (data.length == 0) {
								$('#client_fragment').load("/fragment/" + client_id + "/");
								$('#client_info_edit').show();
								$('#client_info_hide').hide();
							} else { // there was an error
								$('#client_fragment').html(data);
								client_edit_callback();
							}
						},'text');
					});
                });
                return false;
            });

            // Return when they click cancel
            $('.info #client_info_hide').on("click", function(eventObject) {
                $('#client_fragment').load('/fragment/' + client_id + '/');
                $('#client_info_edit').show();
				$('#client_info_hide').hide();
                return false;
            });
            
            //info dialog
            if($('.ui-dialog #client_info_dialog').parent().attr('role')=='dialog') {
				$('.ui-dialog #client_info_dialog').parent().remove();
				$('body>#client_info_dialog').remove();
				
			}
			
            $('.info #client_info_dialog').dialog({
				autoOpen: false,
				model: true,
				minWidth:600,
				position: {my: "right top", at: "left top", of:$(".client-profile")},
				resizable:false,
			});	
			$('.info #client_info_more').click(function () {
				$("#client_info_dialog").dialog("open");
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
				$.post("/note/"+client_id+"/",$('#add_note_form').serialize(),function() {
					load_client(link);
				});
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
				$.post("/visit/"+client_id+"/",$('#add_visit_form').serialize(),function() {
					load_client(link);
				});
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
            
            // remove previous dialogs
			if($('.ui-dialog #end-pregnacy').parent().attr('role')=='dialog') {
				$('.ui-dialog #end-pregnacy').parent().remove();
				$('body>#end-pregnacy').remove();
				
			}
			
			$('.info #end-pregnacy').dialog({
				autoOpen: false,
				model: true,
				buttons: {
					'Ok': function () {
						$.post("/pregnacy/"+client_id+"/",$('#end_pregnacy_form').serialize(),function(response) {
							if(response == "") {
								refresh();
							}
							else {
								$('#end_pregnacy_form').html(response);
								//set date class on end pregnacy form (easy here then in django code)
								$("#end_pregnacy_form #id_end-date").parent().addClass("date");
								setCalendars();
							}
						});
						console.log($('#end_pregnacy_form').serialize())}
				},
				resizable: false,
			});
			$('.info #delivery').click(function () {
				$("#end-pregnacy").dialog("open");
			});
        };
        
        var toggle_msg = function(obj) {
                $(obj).next(".msg_body").slideToggle(600);
                if ($(obj).hasClass('info_expanded')) {
                    $(obj).addClass('info_collapsed').removeClass('info_expanded');
                } else {
                    $(obj).addClass('info_expanded').removeClass('info_collapsed');
                }
            };
        
        // Hook into refresh button
        $("#refresh_button").on('click',function(e) {
			if(client_id) load_client({'id':client_id,'name':client_name});
			refresh();
		});
		
		var refresh = function () {
			if(client_id) load_client({'id':client_id,'name':client_name});
		};
    });
})(jQuery);
