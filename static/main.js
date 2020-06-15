//
//  main functions
//

var SHARK2 = SHARK2 || {};

//
//  set up the system
//
$(document).ready(function () {
    SHARK2.sandboxTest();

    $('#cvsMain')[0].width = 432;
    $('#cvsMain')[0].height = 137;

    SHARK2.context = $('#cvsMain')[0].getContext('2d');
    SHARK2.context.strokeStyle = "#df4b26";
    SHARK2.context.lineJoin = "round";
    SHARK2.context.lineWidth = 5;

    $('#cvsMain').on('mousedown', SHARK2.canvasMouseDown);
    $('#cvsMain').on('mousemove', SHARK2.canvasMouseMove);
    $('#cvsMain').on('mouseup', SHARK2.canvasMouseUp);
});

//
//  sandbox testing specific functions
//
SHARK2.sandboxTest = function () {}

//
//  handling mousedown on the main canvas
//
SHARK2.canvasMouseDown = function (e) {
    SHARK2.coords = [];
    SHARK2.context.clearRect(0, 0, $('#cvsMain').width(), $('#cvsMain').height());
    SHARK2.context.beginPath();

    var rect = $('#cvsMain')[0].getBoundingClientRect();
    SHARK2.context.moveTo(e.clientX - rect.left, e.clientY - rect.top);
    SHARK2.context.stroke();

    SHARK2.isDragging = true;

    SHARK2.coords.push({
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
    })
};

//
//  handling mousemove on the main canvas
//
SHARK2.canvasMouseMove = function (e) {
    if (!SHARK2.isDragging) return;

    var rect = $('#cvsMain')[0].getBoundingClientRect();
    SHARK2.context.lineTo(e.clientX - rect.left, e.clientY - rect.top);
    SHARK2.context.moveTo(e.clientX - rect.left, e.clientY - rect.top);
    SHARK2.context.stroke();

    SHARK2.coords.push({
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
    })
};

//
//  handling mouseup on the main canvas
//
SHARK2.canvasMouseUp = function (e) {
    var rect = $('#cvsMain')[0].getBoundingClientRect();
    SHARK2.coords.push({
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
    })

    console.log(SHARK2.coords)

    $.ajax({
	  type: 'POST',
	  url: '/shark2',
      data: JSON.stringify(SHARK2.coords),
      dataType: "json",
	  success: function(result) {
	    console.log(result);
	    $('#divInfo').html(result['best_word'] + ' ' + result['elapsed_time'])
	  },
	  error: function(result) {
	  }
	});

    SHARK2.isDragging = false;
    SHARK2.context.closePath();
};