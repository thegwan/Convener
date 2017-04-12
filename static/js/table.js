var parsedData;
var requestMid;

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
function getSelected(toServer) {
	var cells = document.getElementsByClassName('selected');

	for (var i = 0; i < cells.length; i++) {
		var daytime = cells[i].id.split("_");
		var day = daytime[0];
		var time = daytime[1];
		toServer.response.push({"day":day, "time":time});
	}
	
}

// remove selected and badtime class from all cells
function clearSelected() {
	var cells = document.getElementsByClassName('cell');
	for (var i = 0; i < cells.length; i++) {
  		cells[i].classList.remove("selected");
  		cells[i].classList.remove("badtime");
	}
}

// Make all the cells unselectable
function makeUnselectable() {
	var cells = document.getElementsByClassName('cell');
	for (var i = 0; i < cells.length; i++) {
  		// cells[i].classList.remove("selected");
  		// cells[i].classList.remove("badtime");
  		$(cells[i]).addClass('unselectable');
	}
	document.getElementById('mainTable').style.cursor = 'not-allowed';
}

// Make all the cells selectable again
function makeSelectable() {
	var cells = document.getElementsByClassName('cell');
	for (var i = 0; i < cells.length; i++) {
  		// cells[i].classList.remove("selected");
  		// cells[i].classList.remove("badtime");
  		cells[i].classList.remove('unselectable');
	}
	document.getElementById('mainTable').style.cursor = 'pointer';
}

// Removes everything from the table, makes the headers what they were on the start screen
// Makes the clear and submit buttons visible again
function resetEverything() {
	makeSelectable();
	clearSelected();
	document.getElementById('tableHeader').innerText = 'Convener';
	document.getElementById('getselected').style.visibility = 'visible';
	document.getElementById('clearselected').style.visibility = 'visible';
	document.getElementById('respondButton').style.visibility = 'hidden';
	document.getElementById('tableSubHeader').innerText = '';
}

// Takes the initial meeting JSON sent by the server and parses it into 
// meetings that can be displayed on the page
function parseInitialData(init_data) {
	resetEverything();
	parsedData = JSON.parse(init_data);
	
	// For displaying the information from my_meetings
	for (var i = 0; i < parsedData['my_meetings'].length; i++){
		var meeting = parsedData['my_meetings'][i];
		// Create a string of who has and hasn't responded
		respString = '';
		notRespString = '';
		for (var j = 0; j < meeting['resp_netids'].length; j++){
			respString += meeting['resp_netids'][j] + ' ';
		}
		for (var k = 0; k < meeting['nresp_netids'].length; k++){
			notRespString += meeting['nresp_netids'][k] + ' ';
		}
		// Creating a div and anchor element to display myMeeting
		var div = document.createElement("DIV");
		// Add a tooltip for when the meeting is hovered over
		$(div).attr('tooltip', "Responded: " + respString + "\n" + " Not Responded: " + notRespString);
		$(div).addClass('tooltipDiv');
		var anchor = document.createElement("A");

		// Function that runs when any myMeeting is clicked
		var f = clickMyMeeting(i, meeting['title']);
		anchor.addEventListener('click', f);

		var textNode = document.createTextNode(meeting['title']);
		anchor.appendChild(textNode);
		div.appendChild(anchor)
		document.getElementById('myMeetingsDiv').appendChild(div);
	}

	// For displaying the information from pending
	for (var i = 0; i < parsedData['pending'].length; i++){
		var meeting = parsedData['pending'][i];
		var div = document.createElement("DIV");

		var anchor = document.createElement("A");

		var f = clickPending(i, meeting['title']);

		anchor.addEventListener('click', f);
		var textNode = document.createTextNode(meeting['title']);
		anchor.appendChild(textNode);
		div.appendChild(anchor)
		document.getElementById('myPendingDiv').appendChild(div);
	}

	// For displaying the information from requested
	for (var i = 0; i < parsedData['my_requests'].length; i++){
		var meeting = parsedData['my_requests'][i];
		var div = document.createElement("DIV");

		var anchor = document.createElement("A");

		var f = clickRequested(i, meeting['title'], meeting['creator'], meeting['mid']);

		anchor.addEventListener('click', f);
		var textNode = document.createTextNode(meeting['title']);
		anchor.appendChild(textNode);
		div.appendChild(anchor)
		document.getElementById('myRequestedDiv').appendChild(div);
	}
}

// Returns an anonymous function that is attached to each item in myMeetings
function clickMyMeeting(i, title) {
	return function() {
		myMeetingClicked(parsedData['my_meetings'][i]['times']);
		document.getElementById('tableHeader').innerText = title;
		document.getElementById('getselected').innerText = 'Submit';
		document.getElementById('respondButton').style.visibility = 'hidden';

	}
};

// When myMeeting is clicked, displays the times and days on the table
function myMeetingClicked(meetingElement) {
	resetEverything();
	fromDaysToTable(meetingElement);
}

// Returns an anonymous function that is attached to each item in pending
function clickPending(i, title) {
	return function() {
		pendingClicked(parsedData['pending'][i]['times']);
		document.getElementById('tableHeader').innerText = title;
		document.getElementById('getselected').style.visibility = 'hidden';
		document.getElementById('clearselected').style.visibility = 'hidden';
		document.getElementById('respondButton').style.visibility = 'hidden';
		document.getElementById('tableSubHeader').innerText = '-Your Response';
		makeUnselectable();
	}
};

// When pending is clicked, displays the user's response times and days on the table
function pendingClicked(meetingElement) {
	resetEverything();
	fromDaysToTable(meetingElement);
}

// Returns an anonymous function that is attached to each item in requested
function clickRequested(i, title, creator, mid) {
	return function() {
		requestedClicked(parsedData['my_requests'][i]['times']);
		document.getElementById('tableHeader').innerText = title;
		document.getElementById('getselected').style.visibility = 'hidden';
		document.getElementById('clearselected').style.visibility = 'visible';
		document.getElementById('respondButton').style.visibility = 'visible';
		document.getElementById('tableSubHeader').innerText = 'Created by: ' + creator;
		requestMid = mid;
	}
};

// When pending is clicked, displays the user's response times and days on the table
function requestedClicked(meetingElement) {
	resetEverything();
	// fromDaysToTable(meetingElement);
}

// Given a list of days and time dicts, changes the table on the main screen 
function fromDaysToTable(listOfDaysAndTimes) {
	clearSelected();
	for (var i = 0; i < listOfDaysAndTimes.length; i++) {
		day = listOfDaysAndTimes[i]['day']
		time = listOfDaysAndTimes[i]['time']
		cell = document.getElementById(day + '_' + time);

		if (! ($(cell).hasClass( "selected"))) {
      		$(cell).addClass("selected");
		}

	}
	// alert('squadala');
}

//--------------------------------------------------------------------------------

// creates JSON containing all selected cells, title, invitees, mid,
// depending on if user responds to or creates a meeting

function createJSON(netid) {
	var toServer = {};
	toServer.netid = netid;
	toServer.response = [];

	// get selected cells
	getSelected(toServer);

	// for meeting creation
	var title = document.getElementById('title').value;
	var responders = document.getElementById('invite').value;

	if (title != '' && responders != '') {
		toServer.title = title                              // js has title property - may cause problems
		toServer.responders = responders.split(/\s*,\s*/);
		document.getElementById('title').value = '';
		document.getElementById('invite').value = '';
	}
	else {
		toServer.mid = requestMid;
	}
	// console.log(toServer)
	$.ajax({
		type: 'POST',
		contentType: 'application/json',
		// Encode data as JSON.
		data: JSON.stringify(toServer),
		dataType: 'text',
		url: '/',
		success: function(){alert('Event Created!');}
	});
	
}

//--------------------------------------------------------------------------------
