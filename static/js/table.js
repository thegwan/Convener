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

// returns an array of selected cells
function getSelected() {
	var cells = document.getElementsByClassName('selected');
	var selectedCells = [];
	for (var i = 0; i < cells.length; i++) {
		selectedCells.push(cells[i].id);
	}
	document.getElementById('selectedCells').innerHTML = selectedCells;
	return selectedCells;
}

// remove selected class from all cells
function clearSelected() {
	var cells = document.getElementsByClassName('cell');
	for (var i = 0; i < cells.length; i++) {
  		cells[i].classList.remove("selected");
	}
}