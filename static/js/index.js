// The parsed JSON that is accessed throughout
var parsedData;

// The meeting id for when the user fills out a request
var requestMid;

// The meeting id for when the user is the creator
var createdMid;

// A dict of key times which each value is the list of people for are available for any given time
var availableDict;

// If we are in a my meeting right now
var inMyMeeting;

// Takes the initial meeting JSON sent by the server and parses it into 
// meetings that can be displayed on the page
function parseInitialData(init_data) {
	// Cleans the screen
	resetEverything();

	// Parses init_data if sent from the initial load
	// leaves the JSON if it comes from the AJAX GET call
	try {
		parsedData = JSON.parse(init_data);
	}
	catch(e) {
		parsedData = init_data;
	}

	// Removes the old meetings that were in the divs
	$('#myRespondedDiv div').remove();
	$('#myMeetingsDiv div').remove();
	$('#myRequestedDiv div').remove();
	
	//------------------------------MY MEETINGS----------------------------------------------------
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
		// Elements where my meetings is to be stored
		var rowDiv = document.createElement("DIV");
		var titleDiv = document.createElement("DIV");
		var starDiv = document.createElement("DIV");
		var textNode = document.createTextNode(meeting['title']);
		
		// Function that runs when any myMeeting is clicked
		var f = clickMyMeeting(i, meeting['title'], 
			meeting['resp_netids'].length, meeting['mid'], 
			meeting['resp_netids'].length + meeting['nresp_netids'].length,
			meeting['finaltime'],
			meeting['creation_date']);
		rowDiv.addEventListener('click', f);

		// Appends children to the DOM objects
		rowDiv.appendChild(titleDiv);
		rowDiv.appendChild(starDiv);
		titleDiv.appendChild(textNode);

		// Adds classes to be styled in css later
		$(rowDiv).addClass('rowDiv tooltipDiv');
		$(titleDiv).addClass('titleDiv col-md-10 col-sm-10 col-xs-10');
		$(starDiv).addClass('starDiv col-md-2 col-sm-2 col-xs-2');

		// Add a tooltip for when the meeting is hovered over
		$(rowDiv).attr('tooltip', "Responded: " + respString + "\n" + " Not Responded: " + notRespString);
		
		// Add a star to the starDiv if the meeting is confirmed
		starDiv.appendChild(createScheduledImage(meeting['finaltime'].length > 0));

		// Corner styling for divs in the meetings lists
		if (i == 0) {
			$(titleDiv).addClass('topLeftDiv');
			$(starDiv).addClass('topRightDiv');
		}
		if (i == parsedData['my_meetings'].length - 1) {
			$(titleDiv).addClass('bottomLeftDiv');
			$(starDiv).addClass('bottomRightDiv');
		}

		// Add the current row to the document
		document.getElementById('myMeetingsDiv').appendChild(rowDiv);
	}

	//---------------------------RESPONDED---------------------------------------------------------
	// For displaying the information from my_responded
	for (var i = 0; i < parsedData['my_responded'].length; i++){
		var meeting = parsedData['my_responded'][i];

		// Elements where responded is to be stored
		var rowDiv = document.createElement("DIV");
		var titleDiv = document.createElement("DIV");
		var starDiv = document.createElement("DIV");
		var textNode = document.createTextNode(meeting['title']);

		// Function to be executed when responded is clicked
		var f = clickMyResponded(i, meeting['title'], 
			meeting['creator'], 
			meeting['finaltime'],
			meeting['creation_date']);
		rowDiv.addEventListener('click', f);

		// Appends children to the DOM objects
		rowDiv.appendChild(titleDiv);
		rowDiv.appendChild(starDiv);
		titleDiv.appendChild(textNode);
		
		// Adds classes to be styled in css later
		$(rowDiv).addClass('rowDiv');
		$(titleDiv).addClass('tooltipDiv titleDiv col-md-10 col-sm-10 col-xs-10');
		$(starDiv).addClass('starDiv col-md-2 col-sm-2 col-xs-2');
		
		// Add a star to the starDiv if the meeting is confirmed
		starDiv.appendChild(createScheduledImage(meeting['finaltime'].length > 0));

		// Corner styling for divs in the meetings lists
		if (i == 0) {
			$(titleDiv).addClass('topLeftDiv');
			$(starDiv).addClass('topRightDiv');
		}
		if (i == parsedData['my_responded'].length - 1) {
			$(titleDiv).addClass('bottomLeftDiv');
			$(starDiv).addClass('bottomRightDiv');
		}

		// Add the current row to the documen
		document.getElementById('myRespondedDiv').appendChild(rowDiv);
	}

	//-----------------------REQUESTED-------------------------------------------------------------
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

		var f = clickRequested(i, meeting['title'],
			meeting['creator'],
			meeting['mid'],
			meeting['creation_date']);

		anchor.addEventListener('click', f);
		var textNode = document.createTextNode(meeting['title']);
		anchor.appendChild(textNode);
		div.appendChild(anchor)
		document.getElementById('myRequestedDiv').appendChild(div);
	}
}

//-------------------------------------------------------------------------------------------------

// Returns an anonymous function that is attached to each item in myMeetings
function clickMyMeeting(i, title, respondedLength, mid, numResponding, finaltime, creationDate) {
	return function() {
		resetEverything();
		rotateTable(creationDate);
		createAvailableDict(parsedData['my_meetings'][i]['responder_times'], numResponding);
		heatmap(parsedData['my_meetings'][i]['responder_times'], respondedLength);
		makeSomeUnselectable();
		
		$('#tableHeader').text(title);
		$('#tableSubHeader').text('Select a final meeting time');

		// Show the submit and delete button
		$('#createMeetingButton').hide();
		$('#clearButton').hide();
		$('#loadPreferredTimesButton').hide();
		$('#submitButton').show();
		$('#deleteMeetingButton').show();
		

		createdMid = mid;
		inMyMeeting = true;

		// Highlights the final time if it has already been selected
		for (var j = 0; j < finaltime.length; j++) {
			var daytime = "#"+finaltime[j]["date"]+"_"+finaltime[j]["time"];
			$(daytime).css('border', '5px solid yellow');
			$(daytime).addClass('selectedColored');
		}
	}
};

// Creates the dict which lists the people who responded to my meeting at a given time
function createAvailableDict (responderTimes, numResponding) {
	availableDict = {};
	var responderKeys = Object.keys(responderTimes);
	for (var i = 0; i < responderKeys.length; i++) {
		var netid = responderKeys[i];
		var times = responderTimes[netid];
		for (var j = 0; j < times.length; j++) {
			var datetime = times[j]['date'] + '_' + times[j]['time'];
			if (datetime in availableDict) {
				availableDict[datetime].push(netid);				
			}
			else {
				availableDict[datetime] = [netid];
			}
		}	
	}
	$('#availableHeader').text('Available: 0/' + numResponding);
	// console.log(availableDict);	
}

// Returns an anonymous function that is attached to each item in requested
function clickRequested(i, title, creator, mid, creationDate) {
	return function() {
		resetEverything();
		rotateTable(creationDate);
		fromDatesToTable(parsedData['my_requests'][i]['times']);
		makeSomeUnselectable();
		$('#tableHeader').text(title);
		$('#tableSubHeader').text('Created by: ' + creator);

		// Show only the clear, loadTimes, and respond buttons
		$('#createMeetingButton').hide();
		$('#respondButton').show();

		document.getElementById('respondButton').style.visibility = 'visible';

		requestMid = mid;
		inMyMeeting = false;
	}
};

// Returns an anonymous function that is attached to each item in responded
function clickMyResponded(i, title, creator, finaltime, creationDate) {
	return function() {
		// When responded is clicked, displays the user's response times and days on the table 
		// after clearing it
		resetEverything();
		rotateTable(creationDate);
		
		var usertimes = parsedData['my_responded'][i]['times'];
		var creatortimes = parsedData['my_responded'][i]['creator_times'];

		responsemap(usertimes, creatortimes)

		// Hide all buttons
		$('#createMeetingButton').hide();
		$('#clearButton').hide();
		$('#loadPreferredTimesButton').hide();
		

		// Modify the title and subheader
		$('#tableHeader').text(title + ' ('+creator+')');
		$('#tableSubHeader').text('-Your Response overlayed on top of creator');
		
		// Makes the rest of the cells unselectable
		makeUnselectable();

		// Highlights the final time if it has already been selected
		for (var j = 0; j < finaltime.length; j++) {
			var daytime = "#"+finaltime[j]["date"]+"_"+finaltime[j]["time"];
			$(daytime).css('border', '5px solid yellow');
		}
		inMyMeeting = false;
	}
};

//--------------------------------- 
// Need another ajax call for user preferred times
// (could integrate into createJSON if u want or just create another one)

// json format: {"netid": netid, "preferredTimes": [lsit of times]}
// preferredTimes in {"day": __, "time:":__} format
//---------------------------------

//-------------------------------------------------------------------------------------------------

// makes creation JSON containing all selected cells, title, responders,
// creationDate, netid

function makeCreationJSON(netid) {
	var toServer = {};
	toServer.category = "creation";
	toServer.netid = netid;
	toServer.response = [];

	// get selected cells, updates toServer.response
	getSelectedDates(toServer);

	// for meeting creation
	var title = document.getElementById('title').value;
	var responders = document.getElementById('invite').value;
	var first = document.getElementsByClassName('cell')[0].id.split("_");
	var creationDate = first[0]

	toServer.title = title
	toServer.responders = responders.split(/\s*,\s*/);
	toServer.creationDate = creationDate

	// clear fields
	document.getElementById('title').value = '';
	document.getElementById('invite').value = '';

	// console.log(toServer)
	$.ajax({
		type: 'POST',
		contentType: 'application/json',
		// Encode data as JSON.
		data: JSON.stringify(toServer),
		dataType: 'text',
		url: '/',
		success: function(){
			displaySnackBar('Event Created');
		}
	});
	// Refresh the page asynchronously
	$.getJSON('/_refreshPage', {

	}, function(data) {
		// alert('at least we made it this far');
		parseInitialData(data);
	});
	resetEverything();
}

//-------------------------------------------------------------------------------------------------

// makes response JSON containing all selected cells, netid, mid,

function makeResponseJSON(netid) {
	var toServer = {};
	toServer.category = "response";
	toServer.netid = netid;
	toServer.response = [];

	// get selected cells, updates toServer.response
	getSelectedDates(toServer);

	toServer.mid = requestMid;

	// console.log(toServer)
	$.ajax({
		type: 'POST',
		contentType: 'application/json',
		// Encode data as JSON.
		data: JSON.stringify(toServer),
		dataType: 'text',
		url: '/',
		success: function(){
			displaySnackBar('Response Submitted');
		}
	});
	// Refresh the page asynchronously
	$.getJSON('/_refreshPage', {

	}, function(data) {
		// alert('at least we made it this far');
		parseInitialData(data);
	});
	resetEverything();
}

//-------------------------------------------------------------------------------------------------

// makes response JSON containing all selected cells, netid, mid,

function makePreferenceJSON(netid) {
	var toServer = {};
	toServer.category = "updatePref";
	toServer.netid = netid;
	toServer.preferredTimes = [];

	// get selected cells, updates toServer.response
	getSelectedDays(toServer);

	// console.log(toServer)
	$.ajax({
		type: 'POST',
		contentType: 'application/json',
		// Encode data as JSON.
		data: JSON.stringify(toServer),
		dataType: 'text',
		url: '/',
		success: function(){
			displaySnackBar('Preferences Submitted');
		}
	});
	// Refresh the page asynchronously
	$.getJSON('/_refreshPage', {

	}, function(data) {
		// alert('at least we made it this far');
		parseInitialData(data);
	});
	resetEverything();
}

// Creates JSON containing the one cell that represents the creator's scheduled time, and
// and mid

function makeFinalJSON(netid) {
	var toServer = {};
	toServer.category = "decision";
	toServer.netid = netid;
	toServer.finalTime = [];

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
		success: function(){
			displaySnackBar('Meeting Scheduled');
		}
	});
	// Refresh the page asynchronously
	$.getJSON('/_refreshPage', {

	}, function(data) {
		// alert('at least we made it this far');
		parseInitialData(data);
	});
	resetEverything();
}

// Creates JSON to delete a meeting. Contains mid and netid

function makeMeetingDeleteJSON(netid) {
	var toServer = {};
	toServer.category = "meetingDelete";
	toServer.netid = netid;
	toServer.mid = createdMid;

	// Server needs to be prepared for this response

	$.ajax({
		type: 'POST',
		contentType: 'application/json',
		// Encode data as JSON.
		data: JSON.stringify(toServer),
		dataType: 'text',
		url: '/',
		success: function(){
			displaySnackBar('Meeting Deleted');
		}
	});
	// Refresh the page asynchronously
	$.getJSON('/_refreshPage', {

	}, function(data) {
		// alert('at least we made it this far');
		parseInitialData(data);
	});
	resetEverything();
}

//-------------------------------------------------------------------------------------------------

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

// Creates an image element that is a checked or unchecked
function createScheduledImage(checked) {
	var image = document.createElement("I");
	$(image).addClass('fa');
	$(image).attr('aria-hidden', 'true');
	$(image).css('font-size', 'inherit');			
	$(image).css('margin-top', '0px');			
	
	if (checked) {
		$(image).addClass('fa-calendar-check-o');
	}
	else {
		$(image).addClass('fa-calendar-times-o');
	}
	return image;
}

// Creates a snackbar with the message msg
function displaySnackBar(msg) {
    $('#snackbar').text(msg);
    $('#snackbar').addClass('show');

    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ $('#snackbar').removeClass('show'); }, 3000);
}

// Hides the modal
function dismissModal() {
	$('#createMeetingModal').modal('hide');
}