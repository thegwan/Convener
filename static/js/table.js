$(document).ready(function() {
	// highlight cells when mousedown
	var $cell = $('.cell').mousedown(function() {
		$(this).toggleClass('selected');
		var flag = $(this).hasClass('selected')
		// while mousedown, highlight cells when mouseenters cell
		$cell.on('mouseenter.selected', function() {
			$(this).toggleClass('selected', flag);
		});
		// highlight final meeting time
		if ($(this).hasClass("colored")) {
  			// Click a colored box to highlight it
  			clearSelectedColored();
  			$(this).removeClass("colored");
  			$(this).addClass("selectedColored");
			$(this).css('border', '5px solid yellow');
			$(this).css('box-sizing', 'border-box'); // border stays inside element
  		}
  		else if ($(this).hasClass("selectedColored")) { // hasClass selectedColored
  			// Unclick to unhighlight
			$(this).css('border', '');
  			$(this).addClass("colored");
  			$(this).removeClass("selectedColored");
  		}   
	});
	$(document).mouseup(function() {
		$cell.off('mouseenter.selected')
	})
});
// previous implementation
// $(document).ready(function() {
// 	// select and unselect clicked-on cells (good time)
//   	$(".cell").click(function(){
//   		if (!($(this).hasClass( "badtime")) && !($(this).hasClass("colored")) && !($(this).hasClass("selectedColored")) ) {
// 	    	if ($(this).hasClass( "selected")) {
// 	      		$(this).removeClass("selected");
// 	   //    		$(this).removeClass('finalSelected');
// 				// $(this).css('background', '');
// 	    	}
// 		    else {
// 				// $(this).addClass('finalSelected');
// 				// $(cell).css('background', 'rgb(0,2,0)');		      	
// 		      	$(this).addClass("selected");
// 	    	};
//   		}
//   		else {
// 	  		if ($(this).hasClass("colored")) {
// 	  			// Click a colored box to highlight it
// 	  			clearSelectedColored();
// 	  			$(this).removeClass("colored");
// 	  			$(this).addClass("selectedColored");
// 				$(this).css('border', '5px solid yellow');
// 	  		}
// 	  		else if ($(this).hasClass("selectedColored")){ // hasClass selectedColored
// 	  			// Unclick to unhighlight
// 				$(this).css('border', '');
// 	  			$(this).addClass("colored");
// 	  			$(this).removeClass("selectedColored");
// 	  		}   			
//   		}
//   	});
//   	// select and unselect double-clicked on cells (bad time)
//   	$(".cell").dblclick(function(){
//   		if (!($(this).hasClass( "selected")) && !($(this).hasClass("colored")) && !($(this).hasClass("selectedColored"))) {
// 	    	if ($(this).hasClass( "badtime")) {
// 	      		$(this).removeClass("badtime");
// 	    	}
// 		    else {
// 		      	$(this).addClass("badtime");
// 	    	};
//   		};
//   	});
// });

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
	// document.getElementById('getselected').style.visibility = 'visible';
	// document.getElementById('clearselected').style.visibility = 'visible';
	// document.getElementById('respondButton').style.visibility = 'hidden';
	// document.getElementById('submitButton').style.visibility = 'hidden';
	$('#tableSubHeader').text('Create Meeting');
	// $('#getselected').text('Create');
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

// Convert a responderTimes into a heatmap on the page where darker colors are better, 
// where responderTimes is a dict of key netid, value times list pairs 
// Gives a weight to each response depending on how many people responded
function heatmap(responderTimes, respondedLength) {
	
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
	//alert(listOfDatesAndTimes.length);
	for (var i = 0; i < listOfDatesAndTimes.length; i++) {
		//console.log(listOfDatesAndTimes);
		day = listOfDatesAndTimes[i]['day']
		time = listOfDatesAndTimes[i]['time']

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
		//day = listOfDatesAndTimes[j]['day'];
		// time = listOfDatesAndTimes[j]['time'];

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

// Given a list of date and time dicts, changes the table on the main screen 
function fromDatesToTable(listOfDatesAndTimes) {
	clearSelected();
	for (var i = 0; i < listOfDatesAndTimes.length; i++) {
		day = listOfDatesAndTimes[i]['date']
		time = listOfDatesAndTimes[i]['time']
		cell = document.getElementById(day + '_' + time);

		if (! ($(cell).hasClass( "selected"))) {
      		$(cell).addClass("selected");
		}

	}
}

// load preferred meeting times
function loadPTimes() {
	clearSelected();

	var cells = document.getElementsByClassName('cell');
	var unselectable = document.getElementsByClassName('unselectable');

	// remove unselectable elements from cells array
	for (var i = 0; i < cells.length; i++) {
		for (var j = 0; j < unselectable.length; j++) {
			if (cells[i] == unselectable[j]) {
				cells.splice(i, 1);
				i--;
			}
		}
	}

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
