function callPythonFunction(sliderValue) {
  $.ajax({
    url: "/run-python-function",
    type: "POST",
    data: { value: sliderValue },
    success: function(response) {
      console.log(response);
    },
    error: function(error) {
      console.log(error);
    }
  });
}
// Add an event listener to the slider
document.getElementById("mySlider").addEventListener("input", function() {
  var sliderValue = this.value;
  callPythonFunction(sliderValue);
});

function resetConnection() {
  $.ajax({
    url: "/reset-connection",
    type: "POST",
    data: {},
    success: function(response) {
      console.log(response);
    },
    error: function(error) {
      console.log(error);
    }
  });
}

$(document).ready(function() {
  
  var layout = {
    width: 500,
    height: 300,
    xaxis: {
      //range: [Date.now() - 60000, Date.now()], // show only the last 60 seconds
      tickformat: 'S', // display time in seconds, e.g. "30s" for 30 seconds ago
    },
    yaxis: {
      tickformat: ',d', // display values as numbers
      title: 'Number of Packets'
    }
  };
  var data = [{ x: [], y: [], type: 'bar', name: 'Sent' },
              { x: [], y: [], type: 'bar', name: 'Received' }];
  Plotly.newPlot('graph', data, layout);

  function updateGraph() {
    $.ajax({
      url: '/get-graph-data',
      type: 'POST',
      success: function(response) {
        var x_sent = response.x_sent;
        var y_sent = response.y_sent;
        var x_received = response.x_received;
        var y_received = response.y_received;

        Plotly.update('graph', { x: [x_sent, x_received], y: [y_sent, y_received] });
      }
    });
  }

  setInterval(updateGraph, 1000);
});
