/* Drop In Content Box script
* Created: May 10th, 2011 by DynamicDrive.com. This notice must stay intact for usage 
* Author: Dynamic Drive at http://www.dynamicdrive.com/
* Visit http://www.dynamicdrive.com/ for full source code
*/

function dropincontentbox(options){
	this.closebutton='<div style="position:absolute;top:4px;right:4px;cursor:pointer"><img src="/kenya/media/closebox.gif" title="Close box" /></div>'
	this.s=jQuery.extend({fx:'easeOutBounce', fxtime:500, freq:'always', showduration:0, pos:['center','center'], deferred:0.5}, options)
	var thisbox=this
	this.s.source=(!$.isArray(this.s.source))? [this.s.source] : this.s.source //convert source option to array
	this.$closebutton=$(this.closebutton).hide().click(function(){thisbox.hide()}) //create and assign behavior to close button
	var loadbox=(this.s.deferred=="fullon")? false: true //var to dictate whether to load drop in box
	this.s.freqispersist=!isNaN(parseInt(this.s.freq))
	if ((this.s.freq=="session" || this.s.freqispersist) && dropincontentbox.routines.getCookie(this.s.source[0])){ //stage 1 check to see if box should not be loaded
		loadbox=false
		if (dropincontentbox.routines.getCookie(this.s.source[0]+'_freq')!=this.s.freq){ //reset cookie and load box if freq setting has been changed
			dropincontentbox.routines.setCookie(this.s.source[0], '', -1) //delete cookie
			loadbox=true
		}
	}
	jQuery(function($){ //on document.ready
		thisbox.init($, thisbox.s, loadbox)
	})
}

dropincontentbox.prototype={

	show:function(pos){
		var $=jQuery, $contentbox=this.$contentbox.css({display:'block'}), s=this.s
		if (typeof pos=="undefined")
			var pos=s.pos
		var winmeasure={w:$(window).width(), h:$(window).height(), left:$(document).scrollLeft(), top:$(document).scrollTop()} //get various window measurements
		var boxmeasure={w:$contentbox.outerWidth(), h:$contentbox.outerHeight()}
		var finalpos=[]
		$.each(pos, function(i, val){
			if (val<0){ //if position value is negative, it means box should be offset from right edge of window
				finalpos[i]=(i==0)? winmeasure.left+winmeasure.w-boxmeasure.w+val : winmeasure.top+winmeasure.h-boxmeasure.h+val
			}
			else if (val=="center"){
				finalpos[i]=(i==0)? winmeasure.left+winmeasure.w/2-boxmeasure.w/2 : winmeasure.top+winmeasure.h/2-boxmeasure.h/2
			}
		})
		$contentbox.css({left:finalpos[0], top:winmeasure.top-boxmeasure.h-10, visibility:'visible'}).animate({top:finalpos[1]}, s.fxduration, s.fx)
	},

	hide:function(){
		this.$contentbox.hide()
		this.$closebutton.hide()
	},

	init:function($, s, loadcheck){
		var thisbox=this
		this.$contentbox=(s.source.length==1)? $(s.source[0]).css({position:'absolute', visibility:'hidden', top:0}).addClass(s.cssclass) : ""
		function selectiveshow(){
			if (loadcheck==false)
				return
			thisbox.$contentbox.append(thisbox.$closebutton).hover( //show close button when mouse hovers over box
				function(){
					thisbox.$closebutton.stop(true,true).fadeIn()
				},
				function(){
					thisbox.$closebutton.stop(true,true).fadeOut()
				}
			) //end hover
			function selectivesetcookie(){
				if (s.freq=="session" || s.freqispersist){
					dropincontentbox.routines.setCookie(s.source[0], 'yes', s.freq)
					dropincontentbox.routines.setCookie(s.source[0]+'_freq', s.freq, s.freq)
				}
			} //END selectivesavecookie
			if (s.deferred>0) //defer loading of box?
				setTimeout(function(){thisbox.show(s.pos); selectivesetcookie()}, s.deferred*1000)
			else if (s.deferred==0){
				thisbox.show(s.pos)
				selectivesetcookie()
			}
			if (s.showduration>0)
				setTimeout(function(){thisbox.hide()}, s.deferred*1000+s.showduration*1000)
		} //END selectiveshow
		if (s.source.length==2){ //if content source is ajax
			$.ajax({
				url: s.source[1].replace(/^http:\/\/[^\/]+\//i, "http://"+window.location.hostname+"/"), //path to external content
				dataType:'html',
				error:function(ajaxrequest){
					alert('Error fetching Ajax content\nServer Response: '+ajaxrequest.responseText)
				},
				success:function(content){
					thisbox.$contentbox=$(content).addClass(s.cssclass).css({position:'absolute', visibility:'hidden', top:0}).appendTo(document.body)
					selectiveshow()
				}
			})// end ajax

		}
		else{
			selectiveshow()
		}
	}
}

dropincontentbox.routines={

	getCookie:function(Name){ 
		var re=new RegExp(Name+"=[^;]+", "i"); //construct RE to search for target name/value pair
		if (document.cookie.match(re)) //if cookie found
			return document.cookie.match(re)[0].split("=")[1] //return its value
		return null
	},

	setCookie:function(name, value, duration){
		var expirestr='', expiredate=new Date()
		if (typeof duration!="undefined"){ //if set persistent cookie
			var offsetmin=parseInt(duration) * (/hr/i.test(duration)? 60 : /day/i.test(duration)? 60*24 : 1)
			expiredate.setMinutes(expiredate.getMinutes() + offsetmin)
			expirestr="; expires=" + expiredate.toUTCString()
		}
		document.cookie = name+"="+value+"; path=/"+expirestr
	}
}