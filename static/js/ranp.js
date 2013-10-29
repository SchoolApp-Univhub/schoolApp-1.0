var thumbnail_class = "col-xs-6 col-sm-4 col-md-3 col-lg-2 user-box"
	function add_thumbnail(id, name, present, image, element) {
		outerdiv = $(document.createElement("div")).addClass(thumbnail_class).data("id",id).data("present",present);
		imgtag = $(document.createElement("img")).addClass('userimg').attr('src',image);
		htag = $(document.createElement("h5")).addClass('name user').text(name);
		thumbnaildiv = $($(document.createElement("div")).addClass("thumbnail user")).append($(imgtag), $(htag));
		if(present == 1){
			$(thumbnaildiv).addClass("present");
		}
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
    		present = $target.data('present');
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
        	$target.data('present',present);
        }
	}
	
	function create_table(list){
		if(list.length > 0){
			rows=list.length;
			columns=list[0].length;
			table=$(document.createElement("table")).addClass("table table-bordered table-hover");
			thead=$(document.createElement("thead"));
			for(columnNo=0; columnNo<columns; columnNo++){
				column=$(document.createElement("th"));
				$(column).text(list[0][columnNo]);
				$(thead).append($(column));
			}
			$(table).append($(thead));
			tbody=$(document.createElement("tbody"));
			for(rowNo=1; rowNo<rows; rowNo++){
				row=$(document.createElement("tr"));
				$(tbody).append($(row));
				for(columnNo=0; columnNo<columns; columnNo++){
					column=$(document.createElement("td"));
					$(column).text(list[rowNo][columnNo]);
					$(row).append($(column));
				}
			}
			$(table).append($(tbody));
		}
		else
			table=null;
		return $(table)
	}
	
	function flash_message(data){
		$( ".flash" ).empty().append( data );
		$(".flash").css('display','block');
	}
