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

_.extend(Backbone.Model.prototype, {
	getView:function() {
		if(typeof(this.view)=="function") {
			if(this.$view) return this.$view.render();
			// no cashed view so make one
			this.$view = new this.view({model:this});
			//console.log("View",this.$view);
			return this.$view.render();
		}
	}
});
_.extend(Backbone.Collection.prototype,{
	getView:Backbone.Model.prototype.getView,
});


var Tools = function() {
	
	var pub = {};//public variables
	//state for currently selected client
	pub.client_id = null;
	
	//Load Client View Into Main Content
	pub.load_client = function(id) {
		pub.client_id = id;
		var fragment_url = "/fragment/display_client/?";
		if(pub.client_id){
			fragment_url += "id="+pub.client_id;
		}
		if($("#select_msg") && $("#select_msg").val() == "list") {
			if (fragment_url.length > 26) { //second get vaiable
				fragment_url += "&";
			}
			fragment_url += "list=1";
		}
		$('#main_content').load(fragment_url,function() {pub.load_client_complete(pub.client_id)});
	}
		
	pub.load_client_complete = function() {
		
		pub.load_message_call_tabs();
		
		 // Change message displays when the user selects the pulldown
		//$('.message_bar .download').html('<a href="/msgcsv/' + pub.client_id + '/">Download</a>');
		$("#select_msg").on("change", pub.load_message_fragment);
		pub.load_message_fragment();
		pub.loadEditHandlers(pub.client_id);
		var now = new Date();
		$('#time').html(now.getHours()+":"+now.getMinutes()+":"+now.getSeconds());
		$('#patient_list #'+pub.client_id).find('.pending').remove();
		$('#patient_list #'+pub.client_id).find('.pending_msg').remove();
	}
        
    //Get the list of messages for current client
	pub.load_message_fragment = function () {
		$(".message-list").load("/fragment/message/" + pub.client_id + "/?mode="+$("#select_msg").val(), function (e) {
			if ($("#select_msg").val() == "conversation") {
				$(".message-list .Client input[type='checkbox']").click(function () {
					var checked = $(this).is(':checked');
					 $.post("/message/prompted/"+$(this).attr('rel')+"/?prompted="+checked); //send post for message promted
					$(this).parent().css('font-weight',(checked)?'bold':'normal');
				});
			}
		});
	}
	
	pub.load_message_call_tabs = function () {
		 // Swap the boxes in add call when the call completed button is changed
		$('#complete').on('change', function(e) {
			pub.toggle_duration_box(this.checked);
		});
		//Swap the boxes in add call when client calls
		$('input[name="initiated"]').change(function(e){
			pub.toggle_duration_box($($('input[name="initiated"]')[1]).checked);
		});
		pub.toggle_duration_box('hide');

		$('#clear_call').on('click', function(e) {
			$('#call_notes').val("");
			$('#complete').attr('checked', false);
			pub.toggle_duration_box('hide');
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
			if (pub.client_id === null || $(".messages #message-box").val() == "") {
				$("#send_message").css("background-color", "rgb(91,141,147)");
				return;
			}
			$.post("/message/" + pub.client_id + "/",$('#message-box').serialize(),function() {
				pub.load_message_fragment();
				$(".messages #message-box").val("").keyup();
				$("#send_message").css("background-color", "rgb(91,141,147)");
			});
		});

		// Save a call when the nurse clicks save
		$('.messages #save_call').on("mousedown", function() {
			$("#save_call").css("background-color", "rgb(217, 233, 236)");
		}).on('mouseup', function() {
			if (pub.client_id == undefined) {
				$("#save_call").css("background-color", "rgb(91,141,147)");
				return;
			}
			//remove duration if not answered
			if(!$('#complete').is(':checked')) {
				$('#duration').val('');
			}
			$.post("/add_call/" + pub.client_id + "/",$('#phone-box').serialize(),function() {
				pub.load_message_fragment();
				$("#save_call").css("background-color", "rgb(91,141,147)");
				$('#call_notes').val("");
				$('#duration').val('');
				$('#complete').attr('checked', false);
				$('#duration_box').hide();
			});
		});
		pub.create_tabs($('.messages #tabs'));
	}
	//end load_message_call_tabs
	
	 pub.load_add_client = function() {
		$('#main_content').load("/add", function() {pub.load_add_client_complete()});
	}
	
	 //Load the add client page into main frame.
	pub.load_add_client_complete = function() {
		pub.setCalendars();
		//randomize day
		$("#id_send_day").val(Math.floor(Math.random()*7));
		$("#add_client_form #submit").click(function () {
			$.post('/add/',$("#add_client_form").serialize(),function (response) {
				if (/^\d+$/.test(response)) { // a single number is the new user id
				window.location = "#client/"+response;
				} else {
					$("#main_content").html(response); 
					pub.load_add_client_complete();
				}
			},'text');
		});
	}
	//End add client setup
	
	pub.load_visit_history = function () {
		console.log("load visit history");
		$('#main_content').load("/visit_history/", function() {pub.load_visit_history_complete()});
	}
	
	//Load Visit History page into main frame
	 pub.load_visit_history_complete = function () {
		pub.setCalendars();
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
	//End Load Visit History

// Utility Functions
	// Switch tabs
	pub.switch_tabs = function(obj) {
		var tabs = $(obj.parents()[2])
		tabs.children('.tab-content').hide();
		tabs.find('.tabs a').removeClass("selected");
		var id = obj.attr("rel");
	 
		$('#'+id).show();
		obj.addClass("selected");
	 }
	 
	 // Create tabs
	 pub.create_tabs = function(obj) {
		// Hook in tab switching
		obj.find('.tabs a').on('click', function(){
			pub.switch_tabs($(this));
		});
		//Set Default Tabs
		obj.find('.defaulttab').each(function(i,ele){pub.switch_tabs($(ele))});
	}
	
	// Adds a date picker to every field marked as being a date
	pub.setCalendars = function() {
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
	
	// Set up the asynchronous search
	var processor = null;
	pub.filter = function() {
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
	
	pub.toggle_msg = function(obj) {
			$(obj).next(".msg_body").slideToggle(600);
			if ($(obj).hasClass('info_expanded')) {
				$(obj).addClass('info_collapsed').removeClass('info_expanded');
			} else {
				$(obj).addClass('info_expanded').removeClass('info_collapsed');
			}
		};
	
	// Toggle call duration box
	pub.toggle_duration_box = function(toggle) {
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
	
//End Utility Functions 

	pub.load_client_list = function() {
		var url = "/fragment/list/?group=";
		url+=$('#group_select').val()+"&sort="+$('#sort_select').val();
		$('#patient_list').load(url,pub.load_client_list_complete);
	}
	
	pub.load_client_list_complete = function() {
		$(".person").on("click", function() {
		   //change css on selected person
		   $(".person_selected").removeClass("person_selected");
		   $(".list #"+this.id).addClass("person_selected");
			//pub.client_id=this.id;
			//pub.load_client();
		});
		people = $('.person');
	   pub.filter();
	}
	
// Load the client editing fragment when they click edit
	 pub.loadEditHandlers = function() {
		//set date class on end pregnacy form (easier here then in django code)
		$("#end_pregnacy_form #id_end-date").parent().addClass("date");
		pub.setCalendars();
		$('.info #client_info_edit').on("click", function(eventObject) {
			$('#client_info_edit').hide();
			$('#client_info_hide').show();
			$('#client_fragment').load("/edit/" + pub.client_id + "/", function client_edit_callback() {
				pub.setCalendars();
				// Save the client when they click save
				$('#client_info_save').on('click', function(e) {
					$.post("/edit/"+pub.client_id+"/",$('#edit_client').serialize(), function(data) {
						if (data.length == 0) {
							$('#client_fragment').load("/fragment/" + pub.client_id + "/");
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
			$('#client_fragment').load('/fragment/' + pub.client_id + '/');
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
					pub.load_client(pub.client_id);
				});
			});
		});

		// Hook in note saving
		$('.info .add_note').on("click", function(eventObject) {
			$.post("/note/"+pub.client_id+"/",$('#add_note_form').serialize(),function() {
				pub.load_client(pub.client_id);
			});
		});

		// Hook in visit adding
		$('.info #visit_add').on("click", function(eventObject) {
			if($(this).parent().hasClass('info_collapsed')){
				pub.toggle_msg($(this).parent())
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
			$.post("/visit/"+pub.client_id+"/",$('#add_visit_form').serialize(),function() {
				pub.load_client(pub.client_id);
			});
		});

		// Hook in visit deleting
		$('.info #visits .delete').each(function(i, e) {
			var pk = $(this).attr('id');
			$(this).on('click', function() {
				$.post("/delete_visit/" + pk + "/", {}, function() {
					pub.load_client(pub.client_id);
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
					$.post("/pregnacy/"+pub.client_id+"/",$('#end_pregnacy_form').serialize(),function(response) {
						if(response == "") {
							pub.load_client(pub.client_id);
						}
						else {
							$('#end_pregnacy_form').html(response);
							//set date class on end pregnacy form (easy here then in django code)
							$("#end_pregnacy_form #id_end-date").parent().addClass("date");
							pub.setCalendars();
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
//end load edit handlers

/**********************
 * Begin Backbone 
 *******************/
	pub.ClientView = Backbone.View.extend({
		className:'person',
		tagName:'a',
		template:_.template($('#tmp_client').html()),
		
		initialize:function() {
			this.listenTo(this.model,'change',this.render);
			this.render();
		},
		
		render:function(evt) {
			//console.log("Render:",this.model.attributes.id)
			this.$el.attr('id',this.model.attributes.id);
			this.$el.attr('href','#client/'+this.model.attributes.id);
			this.$el.html($($.trim(this.template({c:this.model.attributes}))));
			this.$el.click(function(evt){
				console.log(this);
				$('#patient_list .selected').removeClass('selected');
				$(this).addClass('selected');
			});
			return this;
		}
	});
	
	pub.Client = Backbone.Model.extend({
		view:pub.ClientView
	})
	
	pub.ClientsView = Backbone.View.extend({
		initialize:function() {
			this.render();
		},
		
		render:function(evt) {
			var sort = $('#sort_select').val()
			var asc = ($('#sort_direction').hasClass('asc'))?-1:1;
			//Sort the client list
			var clients = this.model.models.sort(function(a,b){
				a = a.get(sort), b=b.get(sort);
				if(a > b) return asc;
				else if(a < b) return asc*-1;
				return 0;// else equal
			});
			//filter the client list based on selected tabs
			$('.patient_bar button').not('.selected').each(function(i,button) {
				console.log($(button).attr('id'));
				clients = clients.filter(function(client) {
					return client.get('study_group')!=$(button).attr('id');
				});
			});
			this.$el.empty();
			clients.forEach(function(client,i){
				this.$el.append(client.getView().el);
			},this);
			return this;
		}
	});
	
	pub.Clients = Backbone.Collection.extend({
		model:pub.Client,
		view:pub.ClientsView,
	});
	
	

	pub.App = Backbone.Router.extend({
		
		routes: {
			'visit_history':pub.load_visit_history,
			'add':pub.load_add_client,
			'client/:id':pub.load_client,
		},
		
	});
/**********************
 * End Backbone 
 *******************/

	return pub;
}

/* Run on Load */
var tools;
$(function() {
	
	tools = Tools();
	
	var app = new tools.App();
	Backbone.history.start();
	
	$('#searchtext').on('keyup', function(e) {
		var code = (e.keyCode ? e.keyCode : e.which);
		if (code == 27) {
			// Clear on escape
			$('#searchtext').val('');
		}
		tools.filter();
	});
	
	$.ajax({
		dataType:'json',
		url:'clients',
		success:function(data){
			tools.clients = new tools.Clients(data);
			$('#patient_list').append(tools.clients.getView().el);
		}
	});
	
	$('#sort_select').change(function(evt){tools.clients.getView().render()});
	$('.patient_bar button').click(function(evt) {
		$(this).toggleClass('selected');
		tools.clients.getView().render();
	});
	$('#sort_direction').click(function(evt) {
		$(this).toggleClass('asc');
		tools.clients.getView().render();
	});

})
