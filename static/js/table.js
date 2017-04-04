// select and unselect clicked-on cells
$(document).ready(function() {
  	$(".cell").click(function(){
    	if ($(this).hasClass( "selected")) {
      		$(this).removeClass("selected");
    	}
	    else {
	      	$(this).addClass("selected");
    	};
  	});
});

// creates JSON containing all selected cells
function getSelected(netid) {
	var cells = document.getElementsByClassName('selected');
	var JSON = '{ "netid" : "' + netid + '", "response" : [';
	for (var i = 0; i < cells.length; i++) {
		var daytime = cells[i].id.split("_");
		var day = daytime[0];
		var time = daytime[1];
		JSON += '{"day" : "' + day + '", "time" : "' + time + '"}';
		if (i != cells.length - 1)
			JSON += ', ';
		else
			JSON += ']}';
	}
	console.log(JSON);
}

// remove selected class from all cells
function clearSelected() {
	var cells = document.getElementsByClassName('cell');
	for (var i = 0; i < cells.length; i++) {
  		cells[i].classList.remove("selected");
	}
}