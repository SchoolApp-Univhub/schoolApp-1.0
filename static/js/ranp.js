    var thumbnail_class = "col-xs-6 col-sm-4 col-md-3 col-lg-2 user-box"
	function add_thumbnail(id, name, present, image, element) {
		outerdiv = $(document.createElement("div")).addClass(thumbnail_class).attr("data-id",id).attr("data-present",present);
		imgtag = $(document.createElement("img")).addClass('userimg').attr('src',image);
		htag = $(document.createElement("h5")).addClass('name user').text(name);
		thumbnaildiv = $($(document.createElement("div")).addClass("thumbnail user")).addClass("present").append($(imgtag), $(htag));
		newdiv=$(outerdiv).append($(thumbnaildiv));
		
        $(element).append(outerdiv);
		set_thumbnail_height($(thumbnaildiv));
        //width = $(thumbnaildiv).css('width');
		//console.log("width="+width);
		//$(thumbnaildiv).css('height',width);
    }
	
	function set_thumbnails_height(){
	    $( "div.thumbnail" ).each(function(){
			set_thumbnail_height($(this))

		});
	}
	
	function set_thumbnail_height(element){
		var width = $(element).css( "width" );
		$(element).css('height',width);		
	}
	
	function student_togglepresence(element){
        var $target=$(element).closest('.user-box');
        if ($target.length == 1){
    		present = $target.attr('data-present');
			$target.children().toggleClass("present");
            if(present==1){
            	console.log("present="+present+".toggling it");
            	present=0;
            }
            else if(present==0){
            	console.log("present="+present+".toggling it");
            	present=1;
            }
        	else console.log("ERROR. user-box present.neither 0 nor 1");
        	$target.attr('data-present',present);
        }
	}
	