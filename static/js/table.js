var parsedData;

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
	parsedData = JSON.parse(init_data);
	
	// For displaying the information from my_meetings
	for (var i = 0; i < parsedData['my_meetings'].length; i++){
		var meeting = parsedData['my_meetings'][i];
		var div = document.createElement("DIV");
		respString = '';
		notRespString = '';
		for (var j = 0; j < meeting['resp_netids'].length; j++){
			respString += meeting['resp_netids'][j] + ' ';
		}
		for (var k = 0; k < meeting['nresp_netids'].length; k++){
			notRespString += meeting['nresp_netids'][k] + ' ';
		}
		$(div).attr('tooltip', "Responded: " + respString + "Not Responded: " + notRespString);
		var anchor = document.createElement("A");
		//$(anchor).attr('onclick', 'myMeetingClicked(anchor)');
		var f = clickMeet(i, meeting['title']);
		// anchor.addEventListener('click', function(i) {
		// 	myMeetingClicked(parsedData['my_meetings'][i]['times']);
		// 	alert('clicked?');
		// }, false);
		anchor.addEventListener('click', f);
		var textNode = document.createTextNode(meeting['title']);
		anchor.appendChild(textNode);
		div.appendChild(anchor)
		document.getElementById('myMeetingsDiv').appendChild(div);
	}

	// fromDaysToTable(parsedData['my_meetings'][1]['times']);
}

// Returns an anonymous function that is attached to each item in myMeetings
function clickMeet(i, title) {
	return function() {
		myMeetingClicked(parsedData['my_meetings'][i]['times']);
		document.getElementById('tableHeader').innerText = title;
		document.getElementById('getselected').innerText = 'Submit';
	}
};

// When myMeeting is clicked, displays the times and days on the table
function myMeetingClicked(meetingElement) {
	// alert(parsedData['confirmed'][0]['creator']);
	fromDaysToTable(meetingElement);
}


// Given a list of days and time dicts, changes the table on the main screen 
function fromDaysToTable(listOfDaysAndTimes) {
	clearSelected();
	for (var i = 0; i < listOfDaysAndTimes.length; i++) {
		day = listOfDaysAndTimes[i]['Day']
		time = listOfDaysAndTimes[i]['Time']
		cell = document.getElementById(day + '_' + time);

		if (! ($(cell).hasClass( "selected"))) {
      		$(cell).addClass("selected");
		}

	}
	// alert('squadala');
}