$(document).ready(function() {

    // Included for POSTS with jquery - DO NOT MODIFY (https://docs.djangoproject.com/en/dev/ref/contrib/csrf/)
    jQuery(document).ajaxSend(function(event, xhr, settings) {
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
        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }
        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });

    $('a').attr('rel','external');

});

function runAction(url) {
    $.ajax({
        url : url,
    });
}

$(function(){
	var menuStatus;
	
	$("a#showMenu").click(function(){
		if(menuStatus != true){				
		$(".ui-page-active").animate({
			marginLeft: "165px",
		  }, 300, function(){menuStatus = true});
		  return false;
		  } else {
			$(".ui-page-active").animate({
			marginLeft: "0px",
		  }, 150, function(){menuStatus = false});
			return false;
		  }
	});

	$('.ui-page').live("swipeleft", function(){
		if (menuStatus){	
		$(".ui-page-active").animate({
			marginLeft: "0px",
		  }, 150, function(){menuStatus = false});
		  }
	});
	
	$('.ui-page').live("swiperight", function(){
		if (!menuStatus){	
		$(".ui-page-active").animate({
			marginLeft: "165px",
		  }, 150, function(){menuStatus = true});
		  }
	});
	
	$("#menu li a").click(function(){
		var p = $(this).parent();
		if($(p).hasClass('active')){
			$("#menu li").removeClass('active');
		} else {
			$("#menu li").removeClass('active');
			$(p).addClass('active');
		}
	});
		
});	
