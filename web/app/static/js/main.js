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

function sendStop() {
  $.ajax({
    url: "/move-stop",
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
function sendMoveForward() {
  $.ajax({
    url: "/move-forward",
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
function sendMoveBackward() {
  $.ajax({
    url: "/move-backward",
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
function sendMoveRight() {
  $.ajax({
    url: "/move-right",
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
function sendMoveLeft() {
  $.ajax({
    url: "/move-left",
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
      url: '/get-graph-data-com',
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


$(document).ready(function() {

  var layout = {
    width: 500,
    height: 500,
    xaxis: {
      title: 'X position',
      autorange: true,
    },
    yaxis: {
      title: 'Y position',
      autorange: true,
    },
    shapes: []
  };

  // Define the data trace for the car position
  var carTrace = {
    x: [0],
    y: [0],
    mode: 'markers',
    marker: {
      size: 10,
      color: 'red'
    }
  };

  // Define the data trace for the obstacles
  var obstacleTrace = {
    x: [],
    y: [],
    mode: 'markers',
    marker: {
      size: 7,
      color: 'blue'
    }
  };

  var data = [carTrace, obstacleTrace];
  Plotly.newPlot('graph-obstacle', data, layout);

  function updateGraph() {
    $.ajax({
      url: '/get-graph-data-obstacle',
      type: 'POST',
      success: function(response) {
             // Extract the obstacle data from the response
        var obstacleData = response.obstacles;
        
        // Update the obstacle trace data
        var obstacleX = obstacleData.map(function(obstacle) {
          return obstacle[0];
        });
        var obstacleY = obstacleData.map(function(obstacle) {
          return obstacle[1];
        });
        Plotly.extendTraces('graph-obstacle', {x: [obstacleX], y: [obstacleY]}, [1]);

        // Update the layout with the obstacle shapes
        layout.shapes = obstacleData.map(function(obstacle) {
          return {
            type: 'circle',
            xref: 'x',
            yref: 'y',
            x0: obstacle[0] - obstacle[2],
            y0: obstacle[1] - obstacle[2],
            x1: obstacle[0] + obstacle[2],
            y1: obstacle[1] + obstacle[2],
            line: {
              color: 'blue'
            }
          };
        });

        // Extract the car position data from the response
        var carPosition = response.carPosition;

        // Update the car trace data
        carTrace.x = [carPosition[0]];
        carTrace.y = [carPosition[1]];
        Plotly.update('graph-obstacle', data, layout);
      }
    
    });
  }


  setInterval(updateGraph, 1000);
});

// Add this to your JavaScript file
setInterval(function() {
  $.ajax({
    url: "/get-status-value", // Change this to the URL of your Flask endpoint
    type: "GET",
    success: function(data) {
      // The Flask endpoint should return a JSON object with a "status" key
      var status = data.status;
  
      var hostIP = $('#host-ip')
      hostIP.text(data.hostIP)

      var hostName = $('#host-name')
      hostName.text( data.hostName)

      
      // Use the status to update the badge text and color
      var badge = $("#badge-status");
      if (status) {
        badge.text("Connected to ESP");
        badge.removeClass("bg-danger");
        badge.addClass("bg-success");
      } else {
        badge.text("No ESP found");
        badge.removeClass("bg-success");
        badge.addClass("bg-danger");
      }
    },
    error: function(jqXHR, textStatus, errorThrown) {
      console.log("Error: " + textStatus);
    }
  });
}, 1000); // Change this to the interval (in milliseconds) at which you want to update the status

function updateIpAddress() {
  fetch('/get-ip-address')
    .then(response => response.json())
    .then(data => {
      const ipAddressElement = document.getElementById('ip-address');
      ipAddressElement.textContent = data.ip_address;
    })
    .catch(error => console.error(error));
}

setInterval(updateIpAddress, 5000);