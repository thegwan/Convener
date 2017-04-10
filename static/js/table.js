$(document).ready(function() {
	// select and unselect clicked-on cells (good time)
  	$(".cell").click(function(){
  		if (! ($(this).hasClass( "badtime"))) {
	    	if ($(this).hasClass( "selected")) {
	      		$(this).removeClass("selected");
	    	}
		    else {
		      	$(this).addClass("selected");
	    	};
  		};
  	});

  	// select and unselect double-clicked on cells (bad time)
  	$(".cell").dblclick(function(){
  		if (! ($(this).hasClass( "selected"))) {
	    	if ($(this).hasClass( "badtime")) {
	      		$(this).removeClass("badtime");
	    	}
		    else {
		      	$(this).addClass("badtime");
	    	};
  		};
  	});
});

// disables create meeting button if no title or responders listed
var checkButton = setInterval(function() {
	if (document.getElementById('title').value == '' ||
		document.getElementById('invite').value == '')
		document.getElementById('modalcreate').disabled = true;
	else
		document.getElementById('modalcreate').disabled = false;
}, 10);

// creates JSON containing all selected cells and title and invitees
function getSelected(netid) {
	var cells = document.getElementsByClassName('selected');

	var responseJSON = {};
	responseJSON.netid = netid;
	responseJSON.response = [];
	for (var i = 0; i < cells.length; i++) {
		var daytime = cells[i].id.split("_");
		var day = daytime[0];
		var time = daytime[1];
		responseJSON.response.push({"day":day, "time":time});
	}
	// console.log(responseJSON);
	var title = document.getElementById('title').value;
	var responders = document.getElementById('invite').value;
	

	if (title != '' && responders != '') {
		responseJSON.title = title
		responseJSON.responders = responders.split(/\s*,\s*/);
		document.getElementById('title').value = '';
		document.getElementById('invite').value = '';
	}

	$.ajax({
		type: 'POST',
		contentType: 'application/json',
		// Encode data as JSON.
		data: JSON.stringify(responseJSON),
		dataType: 'text',
		url: '/',
		success: function(){alert('Event Created!');}
	});
	
}

// remove selected and badtime class from all cells
function clearSelected() {
	var cells = document.getElementsByClassName('cell');
	for (var i = 0; i < cells.length; i++) {
  		cells[i].classList.remove("selected");
  		cells[i].classList.remove("badtime");
	}
}

function parseInitialData(init_data) {
	var parsedData = JSON.parse(init_data);
	alert(parsedData['confirmed']['creator']);
}