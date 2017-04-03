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