$(document).ready(function() {
	// highlight cells when mousedown
	var $cell = $('.cell').mousedown(function() {
		if ($(this).hasClass('unselectable')) {
			return;
		}

		$(this).toggleClass('selected');
		var flag = $(this).hasClass('selected')
		// while mousedown, highlight cells when mouseenters cell
		$cell.on('mouseenter.selected', function() {
			if ($(this).hasClass('unselectable')) {
				return;
			}
			$(this).toggleClass('selected', flag);
		});
		// highlight final meeting time
		if ($(this).hasClass("colored")) {
  			// Click a colored box to highlight it
  			clearSelectedColored();
  			$(this).removeClass("colored");
  			$(this).addClass("selectedColored");
			// $(this).css('border', '5px solid yellow');
			// $(this).css('box-sizing', 'border-box'); // border stays inside element
  		}
  		else if ($(this).hasClass("selectedColored")) { // hasClass selectedColored
  			// Unclick to unhighlight
			// $(this).css('border', '');
  			$(this).addClass("colored");
  			$(this).removeClass("selectedColored");
  		}   
	});
	var $cell = $('.cell').hover(function() {
		if (inMyMeeting) {
			var cellId = $(this).attr('id');
			var aList;
			if (cellId in availableDict) {
				$('#availableList div').remove();
				aList = availableDict[cellId];
				for (var i = 0; i < aList.length; i++) {
					var aDiv = document.createElement("DIV");
					var textNode = document.createTextNode(aList[i]);
					aDiv.appendChild(textNode);

					document.getElementById('availableList').appendChild(aDiv);
				}
			}
			else {
				$('#availableList div').remove();
				aList = [];
			}
			//var oldText = document.getElementById('availableHeader').innerText;
			var oldText = $('#availableHeader').text();
			var startIndex = oldText.indexOf(' ');
			var endIndex = oldText.indexOf('/');
			var p1 = oldText.substring(0, startIndex + 1);
			var p2 = oldText.substring(endIndex, oldText.length);
			$('#availableHeader').text(p1 + aList.length + p2);		
		}
	});
	$(document).mouseup(function() {
		$cell.off('mouseenter.selected')
	});

	// When mainTable header is clicked, highlight the whole column
	$('body').on('click', '#mainTable th', function() {
		// grab the column number
		var column = $(this).attr('data-column');
		var cells_in_column = $('#mainTable td[data-column=' + column + ']');

		if (! cells_in_column.hasClass('unselectable'))
			if (cells_in_column.hasClass('selected'))
				cells_in_column.removeClass('selected');
			else
				cells_in_column.addClass('selected');
		else {
			var hasSelected = cells_in_column.hasClass('selected');
			for (var i = 0; i < cells_in_column.length; i++) {
				if (! cells_in_column[i].classList.contains('unselectable')) {
					if (hasSelected)
						cells_in_column[i].classList.remove('selected');
					else
						cells_in_column[i].classList.add('selected');
				}
			}
		}
	});

	// When prefTable header is clicked, highlight the whole column
	$('body').on('click', '#prefTable th', function() {
		// grab the column number
		var column = $(this).attr('data-column');
		var cells_in_column = $('#prefTable td[data-column=' + column + ']');
		if (! cells_in_column.hasClass('unselectable'))
			if (cells_in_column.hasClass('selected'))
				cells_in_column.removeClass('selected');
			else
				cells_in_column.addClass('selected');
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


// get all selected date cells from main table
function getSelectedDates(toServer) {
	var cells = document.getElementsByClassName('selected');

	for (var i = 0; i < cells.length; i++) {
		var datetime = cells[i].id.split("_");
		var date = datetime[0];
		var time = datetime[1];
		toServer.response.push({"date":date, "time":time});
	}	
}

// get all selected day cells from preference table
function getSelectedDays(toServer) {
	var cells = document.getElementsByClassName('selected');

	for (var i = 0; i < cells.length; i++) {
		var daytime = cells[i].id.split("_");
		var day = daytime[0];
		var time = daytime[1];
		toServer.preferredTimes.push({"day":day, "time":time});
	}	
}

// get the final submit cell
function getSelectedColored(toServer) {
	var cells = document.getElementsByClassName('selectedColored');

	// should be length 1
	for (var i = 0; i < cells.length; i++) {
		var datetime = cells[i].id.split("_");
		var date = datetime[0];
		var time = datetime[1];
		toServer.finalTime.push({"date":date, "time":time});
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
	$(cells[i]).removeClass('selectable');
	for (var i = 0; i < cells.length; i++) {
		if ($(cells[i]).hasClass("selected")) {
			$(cells[i]).removeClass("selected");
  			$(cells[i]).addClass('unselectable');
			// $(cells[i]).addClass("selected");
		}
		else {
  			$(cells[i]).addClass('unselectable');
		}
	}
	document.getElementById('mainTable').style.cursor = 'not-allowed';
}

// Make the white cells unselectable, ignoring selected cells and colored cells 
function makeSomeUnselectable() {
	var cells = document.getElementsByClassName('cell');
	for (var i = 0; i < cells.length; i++) {
  		if (! ($(cells[i]).hasClass("selected") || $(cells[i]).hasClass("colored"))) {
  			$(cells[i]).addClass('unselectable');
			$(cells[i]).removeClass('selectable');
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
		$(cells[i]).addClass('selectable');
	}
	document.getElementById('mainTable').style.cursor = 'pointer';
}

// Removes everything from the table, makes the headers what they were on the start screen
// Makes the clear and submit buttons visible again
function resetEverything() {
	// Makes all the cells selectable and removes their coloring
	makeSelectable();
	clearSelected();
	clearSelectedColored();
	clearColored();

	// Hides the preference table and shows the main table
	$("#prefTable").hide();
	$("#mainTable").show();
	$('#tableHeader').text('Convener');

	// Show only the clear, loadTimes, invert, and create buttons
	$('#respondButton').hide();
	$('#submitButton').hide();
	$('#updatePreferredTimesButton').hide();
	$('#deleteMeetingButton').hide();

	$('#createMeetingButton').show();
	$('#loadPreferredTimesButton').show();
	$('#clearButton').show();
	$('#invertSelectionButton').show();
	
	// Reset the header texts
	$('#tableSubHeader').text('Paint over your available times to create a meeting!');
	$('#tableSubSubHeader').text('');
	$('#availableList div').remove();
	$('#availableHeader').text('');
	inMyMeeting = false;
	neutralizeTable();
}

// Makes it so only one cell can be used in the final submit
function clearSelectedColored() {
	var cells = document.getElementsByClassName('cell');
	for (var i = 0; i < cells.length; i++) {
		if ($(cells[i]).hasClass('selectedColored')) {
	  		$(cells[i]).removeClass("selectedColored");
	  		// $(cells[i]).css('border', '');
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

// overlays user's response on top of creator's response in my_responded
// where userTimes are the user's response, and creatorTimes are the creator's
// response when initially creating the meeting
function responsemap(userTimes, creatorTimes) {
	colors = ['#1AC9FF',
			  '#CCF3FF'];
	clearSelected();
	// convert creatorTimes
	for (var i = 0; i < creatorTimes.length; i++) {
		date = creatorTimes[i]['date'];
		time = creatorTimes[i]['time'];
		cell = document.getElementById(date + '_' + time);
		$(cell).addClass("colored");
		$(cell).css('background', colors[1]);
	}
	// convert userTimes
	for (var i = 0; i < userTimes.length; i++) {
		date = userTimes[i]['date'];
		time = userTimes[i]['time'];
		cell = document.getElementById(date + '_' + time);
		$(cell).addClass("colored");
		$(cell).css('background', colors[0]);
	}

}

// Convert a responderTimes into a heatmap on the page where darker colors are better, 
// where responderTimes is a dict of key netid, value times list pairs 
// Gives a weight to each response depending on how many people responded
function heatmap(responderTimes, respondedLength) {

	var colors = [
				'#00B0E6',
				'#00C3FF',
			    '#1AC9FF',
				'#33CFFF',
				'#4DD5FF',
				'#66DBFF',
				'#80E1FF',
				'#99E7FF',
				'#B3EDFF',
			    '#CCf3FF',
			    '#E6F9FF'
				];

	clearSelected();
	var counts = {};
	listOfDatesAndTimes = [];
	var responderKeys = Object.keys(responderTimes);
	for (var i = 0; i < responderKeys.length; i++) {
		listOfDatesAndTimes = listOfDatesAndTimes.concat(responderTimes[responderKeys[i]]);
	}

	for (var i = 0; i < listOfDatesAndTimes.length; i++) {
		date = listOfDatesAndTimes[i]['date']
		time = listOfDatesAndTimes[i]['time']

		if (counts[date+'_'+time] == null) {
			counts[date+'_'+time] = 1;
		}
		else {
			counts[date+'_'+time] += 1;
		}
	}

	var keys = Object.keys(counts);
	for (var j = 0; j < keys.length; j++) {

		cell = document.getElementById(keys[j]);

		$(cell).addClass("colored");
		if (respondedLength > 1) {
			var interval = 10 / (respondedLength-1);
			$(cell).css('background', colors[10-Math.ceil((counts[keys[j]]-1)*interval)]);
		}
		else
			$(cell).css('background', colors[5]);

	}
}

// Given a list of date and time dicts, changes the table on the main screen 
function fromDatesToTable(listOfDatesAndTimes) {
	clearSelected();
	for (var i = 0; i < listOfDatesAndTimes.length; i++) {
		date = listOfDatesAndTimes[i]['date']
		time = listOfDatesAndTimes[i]['time']
		cell = document.getElementById(date + '_' + time);

		if (! ($(cell).hasClass("selected"))) {
      		$(cell).addClass("selected");
		}
	}
}

// load preferred meeting times
function loadPTimes() {
	clearSelected();
	var cells = document.getElementsByClassName('selectable');

	// format date into day and load preferred meeting times
	for (var i = 0; i < cells.length; i++) {

		var datetime = cells[i].id.split("_");
		var date = datetime[0].split("-");
		var time = datetime[1];

		var month = Number(date[0]);
		var day = Number(date[1]);
		var year = Number(date[2])

		var longdate = new Date(year, month - 1, day);
		var longdayname = String(longdate).split(" ")[0]; // in form Mon, Tue, Wed ...

		// loop through init_data checking if cells[i] is contained in init_data
		for (var j = 0; j < parsedData['my_preferred'].length; j++) {
			var pref_daytime = parsedData['my_preferred'][j];
			var pref_day = pref_daytime['day'];
			var pref_time = pref_daytime['time'];

			if (pref_day == longdayname && pref_time == time)
			{
				cells[i].className += " selected";
			}
		}
	}	
}

// load preferred table (Table_Pref object)
function loadPreferredTable() {
	resetEverything();
	if ($("#prefTable").is(":visible")) {
		$("#prefTable").hide();
		$("#mainTable").show();
	}
	else {
		$("#prefTable").show();
		$("#mainTable").hide();
	}

	// Show only the clear, invert, and updatePreferredTimes buttons
	$('#createMeetingButton').hide();
	$('#loadPreferredTimesButton').hide();
	$('#updatePreferredTimesButton').show();
	$('#invertSelectionButton').show();


	$('#tableHeader').text('Weekly Preferences');
	$('#tableSubHeader').text('Modify your weekly availability!');
	$('#tableSubSubHeader').text('');

	// loop through init_data and put it on the pref_table
	for (var j = 0; j < parsedData['my_preferred'].length; j++) {
		console.log(parsedData['my_preferred'][j]);
		var pref_daytime = parsedData['my_preferred'][j];
		var pref_day = pref_daytime['day'];
		var pref_time = pref_daytime['time'];
		document.getElementById(pref_day + '_' + pref_time).classList.add('selected');
	}
}

// invert selected cells
function invertSelection() {
	var prefTableDisplay = $('#prefTable').css('display');
	var mainTableDisplay = $('#mainTable').css('display');
	
	// ony get the cells of the table that is not hidden
	if (prefTableDisplay == 'none' && mainTableDisplay == 'table')
		allCells = $('#mainTable .cell');
	else if (prefTableDisplay == 'table' && mainTableDisplay == 'none')
		allCells = $('#prefTable .cell');

	for (var i = 0; i < allCells.length; i++) {
		if (! allCells[i].classList.contains('unselectable'))
			allCells[i].classList.toggle('selected');
	}
}

// Moves the main table to display starting from creation date
function rotateTable(creationDate) {
	var headers = $('#mainTable').find('th');
	var dateParts = creationDate.split('-');
	var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
	var days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

	// This year thing will be highly unstable near the edges of a year, but should not break
	myCells = document.getElementsByClassName('cell');
	var firstCellId = myCells[0].id;
	var oldYear = firstCellId.substring(firstCellId.lastIndexOf('-') + 1, firstCellId.indexOf('_'));

	var oldIdsList = [];
	var newIdsList = [];
	var tempIdsList = [];

	for (var i = 0; i < headers.length; i++) {
		var oldTime = headers[i].id;
		var oldDate = oldTime.split('-');

		// Calculate the new data from the creation date and add i days to make the whole table
		var newDate = new Date(dateParts[2],dateParts[0]-1,dateParts[1]);
		newDate.setDate(newDate.getDate() + i);

		$(headers[i]).html(days[newDate.getDay()] + '<br/>' + months[newDate.getMonth()] + '<br/>' + padDigit(newDate.getDate()));
		$(headers[i]).attr('id', days[newDate.getDay()] + '-' + months[newDate.getMonth()] + '-' + padDigit(newDate.getDate()));

		var oldMonth = padDigit(months.indexOf(oldDate[1].trim()) + 1);
		var oldDay = padDigit(oldDate[2]);
		
		var newMonth = padDigit(newDate.getMonth() + 1);
		var newDay = padDigit(newDate.getDate());

		var newDateString = newMonth + '-' + newDay + '-' + oldYear;

		for (var j = 6; j < 12; j++) {
			
			oldIdsList.push(oldMonth + '-' + oldDay + '-' + oldYear + '_' + j + ':00am');
			oldIdsList.push(oldMonth + '-' + oldDay + '-' + oldYear + '_' + j + ':30am');
			
			newIdsList.push(newDateString + '_' + j + ':00am');
			newIdsList.push(newDateString + '_' + j + ':30am');
		}
		for (var j = 1; j <= 12; j++) {
			
			oldIdsList.push(oldMonth + '-' + oldDay + '-' + oldYear + '_' + j + ':00pm');
			oldIdsList.push(oldMonth + '-' + oldDay + '-' + oldYear + '_' + j + ':30pm');
			
			newIdsList.push(newDateString + '_' + j + ':00pm');
			newIdsList.push(newDateString + '_' + j + ':30pm');
		}
	}

	// Populate temporary ids list
	for (var i = 0; i < oldIdsList.length; i++) {
		var tempString = "temp" + i.toString();
		tempIdsList.push(tempString);
		
		document.getElementById(oldIdsList[i]).id = tempString;
	}

	// Convert temporary ids to new ids
	for (var i = 0; i < tempIdsList.length; i++) {
		document.getElementById(tempIdsList[i]).id = newIdsList[i];
	}

}

// Resets the table to start from the current day
function neutralizeTable() {
	var today = new Date();

	var month = padDigit(today.getMonth() + 1);
	var day = padDigit(today.getDate());
	var year = today.getFullYear();

	var todayString = month + '-' + day + '-' + year;

	rotateTable(todayString);
}

// Pads a single digit number with a leading 0, or just returns the number
function padDigit(number) {
	if (number.toString().length == 1) {
		return '0' + number.toString();
	}
	return number.toString();
}
