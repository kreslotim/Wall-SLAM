

/* --------------- ChewBacca Setting -------------- */

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


/* --------------- Movement Function --------------- */
// TODO Simplify in one function
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


/* --------------- Graph Function --------------- */
  
// Com graph TODO FIX ME
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

  setInterval(updateGraph, 10000);
});

// Noise Obstacle Map
$(document).ready(function() {
     // EventSource for receiving SSE events
     var eventSource = new EventSource('/stream-noisy-obstacle');

     // Plotly graph initialization
     var data = [{
       x: [],
       y: [],
       mode: 'markers+lines',
       type: 'scatter',
       marker: {
         size: 5,
         color: 'red',
         symbol: 'circle'
       }
     }, {
       x: [],
       y: [],
       mode: 'markers',
       type: 'scatter',
       marker: {
         size: 1,
         color: 'blue',
         symbol: 'circle-open'
       }
     }];
 
     var layout = {
       title: 'Obstacle Graph',
       xaxis: { title: 'X Coordinate' },
       yaxis: { title: 'Y Coordinate' }
     };
 
     Plotly.newPlot('graph-obstacle', data, layout);
 
     // Event listener for SSE events
     eventSource.onmessage = function(event) {
       var eventData = JSON.parse(event.data);
       var x_car = eventData[0];
       var y_car = eventData[1];
       var x_obs = eventData[2];
       var y_obs = eventData[3];
       var x_del = eventData[4];
       var y_del = eventData[5];


       Plotly.extendTraces('graph-obstacle', { x: [[x_car], x_obs], y: [[y_car], y_obs] }, [0, 1]);
       //Plotly.extendTraces('graph-obstacle', { x: [x_del], y: [y_del] }, [0, 1]);


     };
   
});

/* --------------- Connection Status Checker --------------- */
setInterval(function() {
  $.ajax({
    url: "/get-status-value", // Change this to the URL of your Flask endpoint
    type: "GET",
    success: function(data) {
      // The Flask endpoint should return a JSON object with a "status" key
      var status = data.status;
      var setting = data.setting;
  
      var hostIP = $('#host-ip');
      hostIP.text(data.hostIP);

      var hostName = $('#host-name');
      hostName.text( data.hostName);

      
      // Use the status to update the badge text and color
      const badges = document.querySelectorAll(".connected-badge");
      console.log(badges);
      for (let i = 0; i < badges.length; i++) {
        badge = badges[i];
        if(setting){
          if (status) {
  
            badge.innerHTML=  '<span class="p-2 badge bg-success connected-badge">Connected to ESP</span>';
            
          } else {
            badge.innerHTML=  '<span class="p-2 badge bg-danger connected-badge">No ESP found</span>';
          }
        } else {
          badge.innerHTML=  '<span class="p-2 badge bg-info connected-badge">Connection Setting is off</span>';

  
        }
      }
    },
    error: function(jqXHR, textStatus, errorThrown) {
      console.log("Error: " + textStatus);
    }
  });
}, 1000);

function updateIpAddress() {
  fetch('/get-ip-address')
    .then(response => response.json())
    .then(data => {
      const ipAddressElement = document.getElementById('ip-address');
      ipAddressElement.textContent = data.ip_address;
    })
    .catch(error => console.error(error));
}

setInterval(updateIpAddress, 10000);


/* --------------- Setting Switch --------------- */

function SettingConnectionState() {
  var isChecked = $('#connection-switch').is(':checked');
  var dataESPSwitch = $('#data-ESP-switch');
  var smartMode = $('#mode-smart-switch');
  var dumbMode = $('#mode-dumb-switch');
  

  // Disable the switch and show a message
  $('#connection-switch').prop('disabled', true);
  $('#connection-message').text('Please wait...');
  
  if( !isChecked){
    dataESPSwitch.prop('disabled', true);
    dataESPSwitch.prop('checked', false);
    smartMode.prop('disabled', true);
    smartMode.prop('checked', false);
    dumbMode.prop('disabled', true);
    dumbMode.prop('checked', false);
   
  } else {
    dataESPSwitch.prop('disabled', false);
    dumbMode.prop('disabled', false);
    smartMode.prop('disabled', false);
  }
  sendSwitchSettingState();
  // Wait for 4 seconds before enabling the switch and hiding the message
  setTimeout(function() {
    $('#connection-switch').prop('disabled', false);
    $('#connection-message').text('');
  }, 4000);

}

function SettingDataESP() {
  var isChecked = $('#data-ESP-switch').is(':checked');
  var dataSIMSwitch = $('#data-SIM-switch');
  if( isChecked){
    dataSIMSwitch.prop('disabled', true);
    dataSIMSwitch.prop('checked', false);
  } else {
    dataSIMSwitch.prop('disabled', false);
  }
  sendSwitchSettingState();
}
function SettingDataSIM() {
  var isChecked = $('#data-SIM-switch').is(':checked');
  var dataESPSwitch = $('#data-ESP-switch');
  if( isChecked){
    dataESPSwitch.prop('disabled', true);
    dataESPSwitch.prop('checked', false);
  } else if($('#connection-switch').is(':checked')) {
    dataESPSwitch.prop('disabled', false);
  }
  sendSwitchSettingState();
}
function SettingModeDumb() {
  var isChecked = $('#mode-dumb-switch').is(':checked');
  var modeSmart = $('#mode-smart-switch');

  // Disable the switch and show a message
  $('#mode-dumb-switch').prop('disabled', true);
  $('#mode-dumb-message').text('Please wait...');

  if( isChecked){
    modeSmart.prop('disabled', true);
    modeSmart.prop('checked', false);
  } else if($('#connection-switch').is(':checked')) {
    modeSmart.prop('disabled', false);
  }

  sendSwitchSettingState();

  // Wait for 4 seconds before enabling the switch and hiding the message
  setTimeout(function() {
    $('#mode-dumb-switch').prop('disabled', false);
    $('#mode-smart-switch').prop('disabled', false);
    $('#mode-dumb-message').text('');
  }, 2000);
}
function SettingModeSmart() {
  var isChecked = $('#mode-smart-switch').is(':checked');
  var modeSmart = $('#mode-dumb-switch');

  // Disable the switch and show a message
  $('#mode-smart-switch').prop('disabled', true);
  $('#mode-smart-message').text('Please wait...');

  if( isChecked){
    modeSmart.prop('disabled', true);
    modeSmart.prop('checked', false);
  } else if($('#connection-switch').is(':checked')) {
    modeSmart.prop('disabled', false);
  }

  sendSwitchSettingState();
  // Wait for 4 seconds before enabling the switch and hiding the message
  setTimeout(function() {
    $('#mode-smart-switch').prop('disabled', false);
    $('#mode-dumb-switch').prop('disabled', false);
    $('#mode-smart-message').text('');
  }, 2000);

}

function sendSwitchSettingState() {
  var isCheckedConnection = $('#connection-switch').is(':checked');
  var isCheckedDataESP = $('#data-ESP-switch').is(':checked');
  var isCheckedDataSIM = $('#data-SIM-switch').is(':checked');
  var isCheckedAuto = $('#auto-switch').is(':checked');
  

  $.ajax({
    type: 'POST',
    url: '/update-switch-state-setting',
    data: { 'connection': isCheckedConnection, 'dataESP' : isCheckedDataESP, 'dataSIM' : isCheckedDataSIM, 'auto' : isCheckedAuto },
    dataType: 'json',
    success: function(data) {
      console.log('Switch state updated successfully');
    },
    error: function(xhr, textStatus, errorThrown) {
      console.log('Error updating switch state');
    }
  });
}

/* --------------- Stream Data --------------- */

// create a new EventsourceErrors object to listen for server-sent events
var sourceErrors = new EventSource('/stream-errors');

// add an event listener for when a message is received
sourceErrors.addEventListener('message', function(e) {
  // parse the message data as a JSON object
  var error = JSON.parse(e.data);
  var time = error[0];
  var message = error[1];
  var alertDiv = document.createElement("div");
  alertDiv.classList.add("alert", "alert-danger", "mt-2");
  alertDiv.setAttribute("role", "alert");
  alertDiv.innerHTML = "<strong>" + time + "s </strong>:  " + message;
  var container = document.getElementById("error-container");
  container.insertBefore(alertDiv, container.firstChild);
}, false);

// add an event listener for when the connection is opened
sourceErrors.addEventListener('open', function(e) {
  console.log('SSE connection opened');
}, false);

// add an event listener for when the connection is closed
sourceErrors.addEventListener('error', function(e) {
  console.log('SSE connection closed');
}, false);
 
// create a new EventSource object to listen for server-sent events
var sourceInfo = new EventSource('/stream-info');

// add an event listener for when a message is received
sourceInfo.addEventListener('message', function(e) {
  // parse the message data as a JSON object
  var error = JSON.parse(e.data);
  var time = error[0];
  var message = error[1];
  var alertDiv = document.createElement("div");
  alertDiv.classList.add("alert", "alert-info", "mt-2");
  alertDiv.setAttribute("role", "alert");
  alertDiv.innerHTML = "<strong>" + time + "s </strong>:  " + message;
  var container = document.getElementById("info-container");
  container.insertBefore(alertDiv, container.firstChild);
}, false);

// add an event listener for when the connection is opened
sourceInfo.addEventListener('open', function(e) {
  console.log('SSE connection opened');
}, false);

// add an event listener for when the connection is closed
sourceInfo.addEventListener('error', function(e) {
  console.log('SSE connection closed');
}, false);

// create a new EventSource object to listen for server-sent events
var sourceoutput = new EventSource('/stream-output');

// add an event listener for when a message is received
sourceoutput.addEventListener('message', function(e) {
  // parse the message data as a JSON object
  var error = JSON.parse(e.data);
  var time = error[0];
  var message = error[1];
  var alertDiv = document.createElement("div");
  alertDiv.classList.add("alert", "alert-info", "mt-2");
  alertDiv.setAttribute("role", "alert");
  alertDiv.innerHTML = "<strong>" + time + "s </strong>:  " + message;
  var container = document.getElementById("output-container");
  container.insertBefore(alertDiv, container.firstChild);
}, false);

// add an event listener for when the connection is opened
sourceoutput.addEventListener('open', function(e) {
  console.log('SSE connection opened');
}, false);

// add an event listener for when the connection is closed
sourceoutput.addEventListener('error', function(e) {
  console.log('SSE connection closed');
}, false);

// create a new EventSource object to listen for server-sent events
var sourceinput = new EventSource('/stream-input');

// add an event listener for when a message is received
sourceinput.addEventListener('message', function(e) {
  // parse the message data as a JSON object
  var error = JSON.parse(e.data);
  var time = error[0];
  var message = error[1];
  var alertDiv = document.createElement("div");
  alertDiv.classList.add("alert", "alert-info", "mt-2");
  alertDiv.setAttribute("role", "alert");
  alertDiv.innerHTML = "<strong>" + time + "s </strong>:  " + message;
  var container = document.getElementById("input-container");
  container.insertBefore(alertDiv, container.firstChild);
}, false);

// add an event listener for when the connection is opened
sourceinput.addEventListener('open', function(e) {
  console.log('SSE connection opened');
}, false);

// add an event listener for when the connection is closed
sourceinput.addEventListener('error', function(e) {
  console.log('SSE connection closed');
}, false);

$(document).ready(function() {
  var layout = {
      hovermode: 'closest',
      clickmode: 'event+select',
  };

  $.ajax({
      url: '/refresh_map',
      type: 'GET',
      success: function(data) {
          var chartData = JSON.parse(data);
          var config = { responsive: true };

          Plotly.newPlot('map', chartData, layout, config).then(function(gd) {
              var clickEventFired = true; // Flag to check if click event is fired

              gd.addEventListener('click', function(eventData) {
                  var xaxis = gd._fullLayout.xaxis;
                  var yaxis = gd._fullLayout.yaxis;
                  var x = xaxis.p2l(eventData.x);
                  var y = yaxis.p2l(eventData.y);
                  console.log('Clicked on x:', x, 'y:', y);

                  clickEventFired = false; // Set the flag to true when click event is fired
                                // Check if click event is fired after a short delay
                  setTimeout(function() {
                    if (!clickEventFired) {
                        console.log('Success');
                    }
                }, 100);
              });

              gd.on('plotly_click', function(eventData) {
                setTimeout(function() {
                    var clickedData = eventData.points[0];
                    if (clickedData) {
                      
                        clickEventFired = true; // Set the flag to true when click event is fired
                        // Check if click event is fired after a short delay
                        var traceIndex = clickedData.curveNumber;
                        console.log('Clicked on trace index:', traceIndex);
            
                        // Perform any actions you want when a point on the map is clicked
                        // You can access the clickedData object to retrieve the x and y coordinates
            
                        // Example: Send the clicked coordinates to the server
                        var x = clickedData.x;
                        var y = clickedData.y;
                        console.log('Clicked on x:', x, 'y:', y);
                    } else {
                        console.log('Clicked point is outside any trace');
                    }
                }, 50); // Delay of 100 milliseconds
            });
            


          });
      }
  });
});
