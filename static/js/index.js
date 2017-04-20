var parsedData;
var requestMid;
var createdMid;

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
		// Creating a row div, column divs, and anchor element to display myMeeting
		var rowDiv = document.createElement("DIV");
		var titleDiv = document.createElement("DIV");
		var starDiv = document.createElement("DIV");

		// $(rowDiv).addClass('row');
		$(rowDiv).addClass('rowDiv');

		// Function that runs when any myMeeting is clicked
		var anchor = document.createElement("A");
		var f = clickMyMeeting(i, meeting['title'], meeting['resp_netids'].length, meeting['mid']);
		anchor.addEventListener('click', f);

		var textNode = document.createTextNode(meeting['title']);
		anchor.appendChild(textNode);

		// Add a tooltip for when the meeting is hovered over
		$(titleDiv).attr('tooltip', "Responded: " + respString + "\n" + " Not Responded: " + notRespString);
		titleDiv.appendChild(anchor);
		$(titleDiv).addClass('tooltipDiv titleDiv col-md-10');
		// $(titleDiv).addClass('titleDiv');
		// $(titleDiv).addClass('col-md-10');
		
		// Add a star to the starDiv if the meeting is confirmed
		if (meeting['finaltime'].length > 0) {
			starDiv.appendChild(document.createTextNode('*'));
		}
		else {
			starDiv.appendChild(document.createTextNode('-'));
		}
		$(starDiv).addClass('starDiv col-md-2');
		// $(starDiv).addClass('col-md-2');

		rowDiv.appendChild(titleDiv);
		rowDiv.appendChild(starDiv);
		document.getElementById('myMeetingsDiv').appendChild(rowDiv);
	}

	// For displaying the information from my_responded
	for (var i = 0; i < parsedData['my_responded'].length; i++){
		var meeting = parsedData['my_responded'][i];

		var f = clickMyResponded(i, meeting['title'], meeting['creator'], meeting['finaltime']);

		var rowDiv = document.createElement("DIV");
		var titleDiv = document.createElement("DIV");
		var starDiv = document.createElement("DIV");

		// $(rowDiv).addClass('row');
		$(rowDiv).addClass('rowDiv');

		// var anchor = document.createElement("A");
		// anchor.addEventListener('click', f);
		rowDiv.addEventListener('click', f);
		var textNode = document.createTextNode(meeting['title']);
		titleDiv.appendChild(textNode);

		// titleDiv.appendChild(anchor);
		$(titleDiv).addClass('tooltipDiv titleDiv col-md-10');
		
		// Add a star to the starDiv if the meeting is confirmed
		if (meeting['finaltime'].length > 0) {
			starDiv.appendChild(document.createTextNode('*'));
		}
		else {
			starDiv.appendChild(document.createTextNode('-'));
		}
		$(starDiv).addClass('starDiv col-md-2');

		// Corner styling for divs 
		if (i == 0) {
			$(titleDiv).addClass('topLeftDiv');
			$(starDiv).addClass('topRightDiv');
		}
		else if (i == parsedData['my_responded'].length - 1) {
			$(titleDiv).addClass('bottomLeftDiv');
			$(starDiv).addClass('bottomRightDiv');
		}

		rowDiv.appendChild(titleDiv);
		rowDiv.appendChild(starDiv);
		document.getElementById('myRespondedDiv').appendChild(rowDiv);
	}

	// // For displaying the information from pending
	// for (var i = 0; i < parsedData['pending'].length; i++){
	// 	var meeting = parsedData['pending'][i];
	// 	var div = document.createElement("DIV");

	// 	var anchor = document.createElement("A");

	// 	var f = clickPending(i, meeting['title'], meeting['creator']);

	// 	anchor.addEventListener('click', f);
	// 	var textNode = document.createTextNode(meeting['title']);
	// 	anchor.appendChild(textNode);
	// 	div.appendChild(anchor)
	// 	document.getElementById('myPendingDiv').appendChild(div);
	// }

	// For displaying the information from requested
	var numRequests = parsedData['my_requests'].length;
	if (numRequests <= 0) {
		document.getElementById('requestsBadge').innerHTML = '';
	}
	else {
		document.getElementById('requestsBadge').innerHTML = numRequests;
	}
	for (var i = 0; i < numRequests; i++){
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

// // Takes the JSON info sent by the server and parses it into 
// // meetings that can be displayed on the page
// function parseData(init_data) {
// 	resetEverything();
// 	// parsedData = JSON.parse(init_data);
// 	parsedData = init_data;
// 	// Need to remove everything in the four columns first
// 	$('#myPendingDiv div').remove();
// 	$('#myRequestedDiv div').remove();
// 	$('#myConfirmedDiv div').remove();
// 	$('#myMeetingsDiv div').remove();

// 	// For displaying the information from my_meetings
// 	for (var i = 0; i < parsedData['my_meetings'].length; i++){
// 		var meeting = parsedData['my_meetings'][i];
// 		// Create a string of who has and hasn't responded
// 		respString = '';
// 		notRespString = '';
// 		for (var j = 0; j < meeting['resp_netids'].length; j++){
// 			respString += meeting['resp_netids'][j] + ' ';
// 		}
// 		for (var k = 0; k < meeting['nresp_netids'].length; k++){
// 			notRespString += meeting['nresp_netids'][k] + ' ';
// 		}
// 		// Creating a div and anchor element to display myMeeting
// 		var div = document.createElement("DIV");
// 		// Add a tooltip for when the meeting is hovered over
// 		$(div).attr('tooltip', "Responded: " + respString + "\n" + " Not Responded: " + notRespString);
// 		$(div).addClass('tooltipDiv');
// 		var anchor = document.createElement("A");

// 		// Function that runs when any myMeeting is clicked
// 		var f = clickMyMeeting(i, meeting['title'], meeting['resp_netids'].length, meeting['mid']);
// 		anchor.addEventListener('click', f);

// 		var textNode = document.createTextNode(meeting['title']);
// 		anchor.appendChild(textNode);
// 		div.appendChild(anchor)
// 		document.getElementById('myMeetingsDiv').appendChild(div);
// 	}

// 	// For displaying the information from pending
// 	for (var i = 0; i < parsedData['pending'].length; i++){
// 		var meeting = parsedData['pending'][i];
// 		var div = document.createElement("DIV");

// 		var anchor = document.createElement("A");

// 		var f = clickPending(i, meeting['title'], meeting['creator']);

// 		anchor.addEventListener('click', f);
// 		var textNode = document.createTextNode(meeting['title']);
// 		anchor.appendChild(textNode);
// 		div.appendChild(anchor)
// 		document.getElementById('myPendingDiv').appendChild(div);
// 	}

// 	// For displaying the information from requested
// 	for (var i = 0; i < parsedData['my_requests'].length; i++){
// 		var meeting = parsedData['my_requests'][i];
// 		var div = document.createElement("DIV");

// 		var anchor = document.createElement("A");

// 		var f = clickRequested(i, meeting['title'], meeting['creator'], meeting['mid']);

// 		anchor.addEventListener('click', f);
// 		var textNode = document.createTextNode(meeting['title']);
// 		anchor.appendChild(textNode);
// 		div.appendChild(anchor)
// 		document.getElementById('myRequestedDiv').appendChild(div);
// 	}

// 	// For displaying the information from confirmed
// 	for (var i = 0; i < parsedData['confirmed'].length; i++){
// 		var meeting = parsedData['confirmed'][i];
// 		var div = document.createElement("DIV");

// 		var anchor = document.createElement("A");

// 		var f = clickConfirmed(i, meeting['title'], meeting['creator'], meeting['finaltime']);

// 		anchor.addEventListener('click', f);
// 		var textNode = document.createTextNode(meeting['title']);
// 		anchor.appendChild(textNode);
// 		div.appendChild(anchor)
// 		document.getElementById('myConfirmedDiv').appendChild(div);
// 	}
// }

// Returns an anonymous function that is attached to each item in myMeetings
function clickMyMeeting(i, title, respondedLength, mid) {
	return function() {
		myMeetingClicked(parsedData['my_meetings'][i]['times'], respondedLength);
		$('#tableHeader').text(title);
		$('#getselected').text('Submit');
		document.getElementById('getselected').style.visibility = 'hidden';
		document.getElementById('clearselected').style.visibility = 'hidden';
		document.getElementById('respondButton').style.visibility = 'hidden';
		document.getElementById('submitButton').style.visibility = 'visible';
		$('#tableSubHeader').text('Select a final meeting time');
		createdMid = mid;
	}
};

// When myMeeting is clicked, displays the times and days on the table
function myMeetingClicked(meetingElement, respondedLength) {
	resetEverything();
	heatmap(meetingElement, respondedLength);
}

// // Returns an anonymous function that is attached to each item in pending
// function clickPending(i, title, creator) {
// 	return function() {
// 		pendingClicked(parsedData['pending'][i]['times']);
// 		$('#tableHeader').text(title + ' ('+creator+')');
// 		document.getElementById('getselected').style.visibility = 'hidden';
// 		document.getElementById('clearselected').style.visibility = 'hidden';
// 		document.getElementById('respondButton').style.visibility = 'hidden';
// 		$('#tableSubHeader').text('-Your Response');
// 		makeUnselectable();
// 	}
// };

// // When pending is clicked, displays the user's response times and days on the table
// function pendingClicked(meetingElement) {
// 	resetEverything();
// 	fromDaysToTable(meetingElement);
// }

// Returns an anonymous function that is attached to each item in requested
function clickRequested(i, title, creator, mid) {
	return function() {
		requestedClicked(parsedData['my_requests'][i]['times']);
		$('#tableHeader').text(title);
		document.getElementById('getselected').style.visibility = 'hidden';
		document.getElementById('clearselected').style.visibility = 'visible';
		document.getElementById('respondButton').style.visibility = 'visible';
		$('#tableSubHeader').text('Created by: ' + creator);
		requestMid = mid;
	}
};

// When pending is clicked, displays the user's response times and days on the table
function requestedClicked(meetingElement) {
	resetEverything();
	fromDaysToTable(meetingElement);
	makeSomeUnselectable();
}

// Returns an anonymous function that is attached to each item in responded
function clickMyResponded(i, title, creator, finaltime) {
	return function() {
		respondedClicked(parsedData['my_responded'][i]['times']);
		$('#tableHeader').text(title + ' ('+creator+')');
		document.getElementById('getselected').style.visibility = 'hidden';
		document.getElementById('clearselected').style.visibility = 'hidden';
		$('#tableSubHeader').text('-Your Response');
		makeUnselectable();
		for (var j = 0; j < finaltime.length; j++) {
			var daytime = "#"+finaltime[j]["day"]+"_"+finaltime[j]["time"];
			$(daytime).css('border', '5px solid yellow');
		}
		
	}
};

// When responded is clicked, displays the user's response times and days on the table
function respondedClicked(meetingElement) {
	resetEverything();
	fromDaysToTable(meetingElement);
}


//--------------------------------- 
// Need another ajax call for user preferred times
// (could integrate into createJSON if u want or just create another one)

// json format: {"netid": netid, "preferredTimes": [lsit of times]}
// preferredTimes in {"day": __, "time:":__} format
//---------------------------------

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
		success: function(){
			if (toServer.hasOwnProperty('mid')) {
				alert('Response Submitted');
			}
			else {
				alert('Event Created!');
			}
		}
	});
	// Refresh the page asynchronously
	$.getJSON('/_refreshPage', {

	}, function(data) {
		// alert('at least we made it this far');
		parseData(data);
	});
	resetEverything();
}


// Creates JSON containing the one cell that represents the creator's scheduled time, and
// and mid

function createFinalJSON(netid) {
	var toServer = {};
	toServer.netid = netid;
	toServer.finalTime = [];

	// get selected cells
	//getSelected(toServer);

	// Gets the selectedColored cell
	getSelectedColored(toServer);

	toServer.mid = createdMid;

	// Server needs to be prepared for this response

	$.ajax({
		type: 'POST',
		contentType: 'application/json',
		// Encode data as JSON.
		data: JSON.stringify(toServer),
		dataType: 'text',
		url: '/',
		success: function(){alert('Meeting Scheduled');}
	});
	// Refresh the page asynchronously
	$.getJSON('/_refreshPage', {

	}, function(data) {
		// alert('at least we made it this far');
		parseData(data);
	});
	resetEverything();
}

//--------------------------------------------------------------------------------

function dropdown() {
    document.getElementById("myRequestedDiv").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(e) {
  if (!e.target.matches('.requestsAnchor')) {
    var myDropdown = document.getElementById("myRequestedDiv");
      if (myDropdown.classList.contains('show')) {
        myDropdown.classList.remove('show');
      }
  }
}