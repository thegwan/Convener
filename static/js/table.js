var parsedData;
var requestMid;
var createdMid;

$(document).ready(function() {
	// select and unselect clicked-on cells (good time)
  	$(".cell").click(function(){
  		if (!($(this).hasClass( "badtime")) && !($(this).hasClass("colored")) && !($(this).hasClass("selectedColored")) ) {
	    	if ($(this).hasClass( "selected")) {
	      		$(this).removeClass("selected");
	   //    		$(this).removeClass('finalSelected');
				// $(this).css('background', '');
	    	}
		    else {
				// $(this).addClass('finalSelected');
				// $(cell).css('background', 'rgb(0,2,0)');		      	
		      	$(this).addClass("selected");
	    	};
  		}
  		else {
	  		if ($(this).hasClass("colored")) {
	  			// Click a colored box to highlight it
	  			clearSelectedColored();
	  			$(this).removeClass("colored");
	  			$(this).addClass("selectedColored");
				$(this).css('border', '5px solid yellow');
	  		}
	  		else if ($(this).hasClass("selectedColored")){ // hasClass selectedColored
	  			// Unclick to unhighlight
				$(this).css('border', '');
	  			$(this).addClass("colored");
	  			$(this).removeClass("selectedColored");
	  		}   			
  		}
  	});
  	// select and unselect double-clicked on cells (bad time)
  	$(".cell").dblclick(function(){
  		if (!($(this).hasClass( "selected")) && !($(this).hasClass("colored")) && !($(this).hasClass("selectedColored"))) {
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

// creates JSON with the final submit cell
function getSelectedColored(toServer) {
	var cells = document.getElementsByClassName('selectedColored');

	for (var i = 0; i < cells.length; i++) {
		var daytime = cells[i].id.split("_");
		var day = daytime[0];
		var time = daytime[1];
		toServer.finalTime.push({"day":day, "time":time});
	}
	
}

// remove selected and badtime class from all cells
function clearSelected() {
	var cells = document.getElementsByClassName('cell');
	for (var i = 0; i < cells.length; i++) {
  		cells[i].classList.remove("selected");
  		cells[i].classList.remove("badtime");
  		$(cells[i]).removeAttr('style');
	}
}

// Make all the cells unselectable
function makeUnselectable() {
	var cells = document.getElementsByClassName('cell');
	for (var i = 0; i < cells.length; i++) {
		if ($(cells[i]).hasClass( "selected")) {
			$(cells[i]).removeClass("selected");
  			$(cells[i]).addClass('unselectable');
			$(cells[i]).addClass("selected");
		}
		else {
  			$(cells[i]).addClass('unselectable');
		}
	}
	document.getElementById('mainTable').style.cursor = 'not-allowed';
}

// Make the white cells unselectable
function makeSomeUnselectable() {
	var cells = document.getElementsByClassName('cell');
	for (var i = 0; i < cells.length; i++) {
  		if (! ($(cells[i]).hasClass( "selected"))) {
  			$(cells[i]).addClass('unselectable');
  		}
  		else {
  			$(cells[i]).removeClass('selected');
  		}
	}
}

// Make all the cells selectable again
function makeSelectable() {
	var cells = document.getElementsByClassName('cell');
	for (var i = 0; i < cells.length; i++) {
  		cells[i].classList.remove('unselectable');
	}
	document.getElementById('mainTable').style.cursor = 'pointer';
}

// Removes everything from the table, makes the headers what they were on the start screen
// Makes the clear and submit buttons visible again
function resetEverything() {
	makeSelectable();
	clearSelected();
	clearSelectedColored();
	clearColored();
	$('#tableHeader').text('Convener');
	document.getElementById('getselected').style.visibility = 'visible';
	document.getElementById('clearselected').style.visibility = 'visible';
	document.getElementById('respondButton').style.visibility = 'hidden';
	document.getElementById('submitButton').style.visibility = 'hidden';
	$('#tableSubHeader').text('Create Meeting');
	$('#getselected').text('Create');
}

// Makes it so only one cell can be used in the final submit
function clearSelectedColored() {
	var cells = document.getElementsByClassName('cell');
	for (var i = 0; i < cells.length; i++) {
		if ($(cells[i]).hasClass('selectedColored')) {
	  		$(cells[i]).removeClass("selectedColored");
	  		$(cells[i]).css('border', '');
			$(cells[i]).addClass("colored");
		}
	}
}

// Removes the colored class from all cells
function clearColored() {
	var cells = document.getElementsByClassName('cell');
	for (var i = 0; i < cells.length; i++) {
		if ($(cells[i]).hasClass('colored')) {
	  		$(cells[i]).removeClass("colored");
		}
	}
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
		var f = clickMyMeeting(i, meeting['title'], meeting['resp_netids'].length, meeting['mid']);
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

		var f = clickPending(i, meeting['title'], meeting['creator']);

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

	// For displaying the information from confirmed
	for (var i = 0; i < parsedData['confirmed'].length; i++){
		var meeting = parsedData['confirmed'][i];
		var div = document.createElement("DIV");

		var anchor = document.createElement("A");

		var f = clickConfirmed(i, meeting['title'], meeting['creator'], meeting['finaltime']);

		anchor.addEventListener('click', f);
		var textNode = document.createTextNode(meeting['title']);
		anchor.appendChild(textNode);
		div.appendChild(anchor)
		document.getElementById('myConfirmedDiv').appendChild(div);
	}
}

// Takes the JSON info sent by the server and parses it into 
// meetings that can be displayed on the page
function parseData(init_data) {
	resetEverything();
	// parsedData = JSON.parse(init_data);
	parsedData = init_data;
	// Need to remove everything in the four columns first
	$('#myPendingDiv div').remove();
	$('#myRequestedDiv div').remove();
	$('#myConfirmedDiv div').remove();
	$('#myMeetingsDiv div').remove();

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
		var f = clickMyMeeting(i, meeting['title'], meeting['resp_netids'].length, meeting['mid']);
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

		var f = clickPending(i, meeting['title'], meeting['creator']);

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

	// For displaying the information from confirmed
	for (var i = 0; i < parsedData['confirmed'].length; i++){
		var meeting = parsedData['confirmed'][i];
		var div = document.createElement("DIV");

		var anchor = document.createElement("A");

		var f = clickConfirmed(i, meeting['title'], meeting['creator'], meeting['finaltime']);

		anchor.addEventListener('click', f);
		var textNode = document.createTextNode(meeting['title']);
		anchor.appendChild(textNode);
		div.appendChild(anchor)
		document.getElementById('myConfirmedDiv').appendChild(div);
	}
}

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

// Returns an anonymous function that is attached to each item in pending
function clickPending(i, title, creator) {
	return function() {
		pendingClicked(parsedData['pending'][i]['times']);
		$('#tableHeader').text(title + ' ('+creator+')');
		document.getElementById('getselected').style.visibility = 'hidden';
		document.getElementById('clearselected').style.visibility = 'hidden';
		document.getElementById('respondButton').style.visibility = 'hidden';
		$('#tableSubHeader').text('-Your Response');
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

// Returns an anonymous function that is attached to each item in confirmed
function clickConfirmed(i, title, creator, finaltime) {
	return function() {
		confirmedClicked(parsedData['confirmed'][i]['times']);
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

// When confirmed is clicked, displays the user's response times and days on the table
function confirmedClicked(meetingElement) {
	resetEverything();
	fromDaysToTable(meetingElement);
}

// Convert a listOfDaysAndTimes into a heatmap on the page where darker colors are better
// Gives a weight to each response depending on how many people responded
function heatmap(listOfDaysAndTimes, respondedLength) {
	
	// var colors = ['#24C904',  // most green
	// 			  '#6ECF07',
	// 			  '#87D008',
	// 			  '#A0D209',
	// 			  '#D3D60A',  // yellowish
	// 			  '#D8C20B',
	// 			  '#D9AC0C',
	// 			  '#DB950D',
	// 			  '#DD7F0E',
	// 			  '#DF680F']  // most orange
	var colors = ['#0ABD21',  // most green
				  '#17E731',
				  '#2EE945',
				  '#45EC59',
				  '#5CEE6D',  
				  '#74F182',
				  '#8BF396',
				  '#A2F5AA',
				  '#B9F8BE',
				  '#E8FDE7']  // most whitish
	clearSelected();
	var counts = {};
	// var weight = 20;
	// 250 max r and b values, 
	// var weight = Math.ceil(255 / respondedLength);
	// if (respondedLength >= 30) {
	// 	weight = 1;
	// }
	//alert(listOfDaysAndTimes.length);
	for (var i = 0; i < listOfDaysAndTimes.length; i++) {
		//console.log(listOfDaysAndTimes);
		day = listOfDaysAndTimes[i]['day']
		time = listOfDaysAndTimes[i]['time']

		if (counts[day+'_'+time] == null) {
			counts[day+'_'+time] = 1;
		}
		else {
			counts[day+'_'+time] += 1;
		}
	}
	// alert(counts);
	var keys = Object.keys(counts);
	//alert(keys.length);
	for (var j = 0; j < keys.length; j++) {
		//day = listOfDaysAndTimes[j]['day'];
		// time = listOfDaysAndTimes[j]['time'];

		cell = document.getElementById(keys[j]);
		//alert(day + '_' + time);
		shade = counts[keys[j]] / respondedLength;
		// redAndBlue = Math.floor(255 - weight * counts[keys[j]]);
		// if (redAndBlue < 0) {
		// 	redAndBlue = 0;
		// }
		// green = 238 - weight * counts[keys[j]];
		// if (green < 50) {
		// 	green = 50;
		// }
		// $(cell).css('background', 'rgb(0,' + Math.floor(green) + ',0)');
		
		$(cell).addClass("colored");
		$(cell).css('background', colors[10-Math.ceil(shade*10)]);
	}
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
