$(document).ready(function() {
	// select and unselect clicked-on cells (good time)
  	$(".cell").click(function(){
    	if ($(this).hasClass( "selected")) {
      		$(this).removeClass("selected");
    	}
	    else {
	      	$(this).addClass("selected");
    	};
  	});

  	// select and unselect double-clicked on cells (bad time)
  	$(".cell").dblclick(function(){
    	if ($(this).hasClass( "badtime")) {
      		$(this).removeClass("badtime");
    	}
	    else {
	      	$(this).addClass("badtime");
    	};
  	});
});

// creates JSON containing all selected cells
function getSelected(netid) {
	var cells = document.getElementsByClassName('selected');
	var responseJSON = '{ "netid" : "' + netid + '", "response" : [';
	for (var i = 0; i < cells.length; i++) {
		var daytime = cells[i].id.split("_");
		var day = daytime[0];
		var time = daytime[1];
		responseJSON += '{"day" : "' + day + '", "time" : "' + time + '"}';
		if (i != cells.length - 1)
			responseJSON += ', ';	
	}
	responseJSON += ']}';
	$.ajax({
		type: 'POST',
		contentType: 'application/json',
		// Encode data as JSON.
		data: JSON.stringify(responseJSON),
		dataType: 'text',
		url: '/',
		success: function(){alert('submitted!');}
	});
	console.log(JSON);
}

// remove selected and badtime class from all cells
function clearSelected() {
	var cells = document.getElementsByClassName('cell');
	for (var i = 0; i < cells.length; i++) {
  		cells[i].classList.remove("selected");
  		cells[i].classList.remove("badtime");
	}
}