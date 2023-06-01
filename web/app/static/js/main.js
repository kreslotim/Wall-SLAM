

/* --------------- Movement Function ---------KmeansGyro------ */
function sendMovementCommand(direction) {
  var debugStatus = document.getElementById("debugStatus");
  $.ajax({
    url: "/post-move",
    type: "POST",
    data: { direction: direction },
    success: function(response) {
      var message = response.message;
      var alertClass = response.espStatus == 200 ? "alert-success" : "alert-danger";
      var alertHTML = '<div class="alert ' + alertClass + '">' + message + '</div>';
      debugStatus.innerHTML = alertHTML;
       // Automatically hide the alert after 5 seconds
       setTimeout(function() {
        debugStatus.innerHTML = '';
      }, 2000);
    },
    error: function(error) {
      console.log(error);
    }
  });
}

/* --------------- Graph Function --------------- */
  
$(document).ready(function() {
  initGraphCom(); // Call the function to initialize the graph
  initGraphRedundancy();
  initGraphNoise();
  initKmeanGraph();
  initKmeanSlider();
  initDistance();
  initMouvement();
});


function toggleUpdate(name, updateFunction) {
  var progressIntervalId; // Variable to hold the progress interval ID
  var progressValue = 0; // Current progress value
  var intervalId; // Variable to hold the interval ID

  // Update Label
  const sf = document.getElementById('slider-frequency-' + name);
  const lf = document.getElementById('label-frequency-'+ name);
  sf.addEventListener('change', function() {
    lf.innerText = this.value;
  });

  // Function to update the progress bar
  function updateProgressBar() {
    progressValue += 10; // Increase progress value by 10
    if (progressValue >= 100) progressValue = 0;
    document.getElementById('pb-' + name).style.width = progressValue + '%'; // Update progress bar width
    document.getElementById('pb-' + name).innerHTML = progressValue + '%';
    document.getElementById('pb-' + name).setAttribute('aria-valuenow', progressValue); // Update aria-valuenow attribute
    if (!intervalId) {
      clearInterval(progressIntervalId); // Clear the progress interval when it reaches 100%
      progressValue = 0; // Reset progress value
      document.getElementById('pb-' + name).style.width = '0%'; // Reset progress bar width
      document.getElementById('progress-'+ name).style.display = 'none'; // Hide the progress bar
    }
  }

  // Toggle button event listener
  document.getElementById('tg-update-' + name).addEventListener('click', function() {
    if (intervalId) {
      // If interval is active, clear it and deactivate the toggle button
      clearInterval(intervalId);
      intervalId = null;
      clearInterval(progressIntervalId);
      this.innerHTML = 'Toggle Update';
      var progressContainers = document.getElementById('progress-'+ name);
      progressContainers.style.display = 'none'; // Hide the progress bar
      document.getElementById('pb-' + name).style.width = '0%'; // Reset progress bar width
      document.getElementById("tg-update-"+ name).classList.add('tg-update');
      document.getElementById('progress-'+ name).classList.add('pdiv');
      document.getElementById('pb-'+ name).classList.add('pb');
      document.getElementById('label-frequency-'+ name).classList.add('label-frequency');
      document.getElementById('slider-frequency-'+ name).classList.add('slider-frequency');

      progressValue = 0; // Reset progress value
    } else {
      const updateSlider = document.getElementById('slider-frequency-' + name).value;
      timeInterval = parseInt(updateSlider) * 1000;
      console.log(timeInterval);
      // If interval is inactive, start it and activate the toggle button
      intervalId = setInterval(updateFunction, timeInterval);
      progressIntervalId = setInterval(updateProgressBar, timeInterval / 10); // Update progress bar every 10% of the timeInterval
      this.innerHTML = 'Stop Update';
      document.getElementById('progress-'+name).style.display = 'block'; // Show the progress bar
      document.getElementById('progress-'+ name).classList.remove('pdiv');
      document.getElementById('pb-'+ name).classList.remove('pb');
      document.getElementById("tg-update-"+ name).classList.remove('tg-update');
      document.getElementById('label-frequency-'+ name).classList.remove('label-frequency');
      document.getElementById('slider-frequency-'+ name).classList.remove('slider-frequency');
    }
  });
}



function initDistance(){


  toggleUpdate("distance",updateMap);
    // Sample data
    var time = []; // Time points
    var mag = []; // Distance values for series 1
    var gyro = []; // Distance values for series 2
    var kalman = []; // Distance values for series 3
  
    // Data traces
    var magTrace = {
      x: time,
      y: mag,
      mode: 'lines',
      name: 'Mag'
    };
  
    var gyroTrace = {
      x: time,
      y: gyro,
      mode: 'lines',
      name: 'Gyro'
    };
  
    var kalmanTrace = {
      x: time,
      y: kalman,
      mode: 'lines',
      name: 'Kalman'
    };
  
    // Layout configuration
    var layout = {
      xaxis: {
        title: 'Time'
      },
      yaxis: {
        title: 'Orientation'
      },
      margin: {
        t: 10, // Top margin
        l: 40, // Left margin
        r: 20, // Right margin
        b: 40  // Bottom margin
      },
    };
  
    // Combine the traces into an array
    var data = [magTrace, gyroTrace, kalmanTrace];
  
    // Create the line chart
    Plotly.newPlot('graph-distance', data, layout, { displayModeBar: false });
  function updateMap() {
    $.ajax({
      url: '/get-graph-distance',
      type: 'GET',
      success: function(data) {
           var newChartData = JSON.parse(data.data);

            time = newChartData.time;
            magTrace.y = newChartData.mag;
            magTrace.x = time;
            gyroTrace.y = newChartData.gyro;
            gyroTrace.x= time;
            kalmanTrace.y = newChartData.kalman;
            kalmanTrace.x = time;
            data = [magTrace, gyroTrace, kalmanTrace];
            console.log(data)
           
           Plotly.newPlot('graph-distance', data, layout);
        }
      
    });
  }
  function reset(){
    var noData = [];
    Plotly.newPlot('graph-distance', noData, layout, { displayModeBar: false });
  }
  // Call updateMap() when the button is clicked
  $('#update-distance').click(function() {
    updateMap();
  })
  $('#reset-distance').click(function() {
    reset();
  })
  return [updateMap, reset];
  }

function initGraphCom() {
  toggleUpdate("com",updateMap);
  var layout = {
    xaxis: {
      //range: [Date.now() - 60000, Date.now()], // show only the last 60 seconds
      tickformat: 'S', // display time in seconds, e.g. "30s" for 30 seconds ago
    },
    yaxis: {
      tickformat: ',d', // display values as numbers
      title: 'Number of Packets'
    },
    margin: {
      t: 10, // Top margin
      l: 40, // Left margin
      r: 20, // Right margin
      b: 40  // Bottom margin
    },
  };
  var data = [
    { x: [], y: [], type: 'bar', name: 'Sent' },
    { x: [], y: [], type: 'bar', name: 'Received' },
    { x: [], y: [], type: 'bar', name: 'Obstacle Detected' }
  ];
  
  Plotly.newPlot('graph-com', data, layout, { displayModeBar: false });
  function updateMap() {
    $.ajax({
      url: '/get-graph-com',
      type: 'GET',
      success: function(response) {
      
        var newChartData = JSON.parse(response.data);
      var sentData = newChartData.sent;
      var receivedData = newChartData.received;
      var obstacleData = newChartData.obs;

      // Find the minimum and maximum values of the received data
      var minReceived = Math.floor(Math.min(...receivedData));
      var maxReceived = Math.floor(Math.max(...receivedData));
      
      // Create the x-axis values as an array of seconds
      var seconds = [];
      for (var i = minReceived; i <= maxReceived; i++) {
        seconds.push(i);
      }
      


      
      var sentValues = countPoints(sentData, seconds);
      var receivedValues = countPoints(receivedData, seconds);
      var obsValues = countPoints(obstacleData,seconds)

      var data = [
        { x: seconds, y: sentValues, type: 'bar', name: 'Sent' },
        { x: seconds, y: receivedValues, type: 'bar', name: 'Received' },
        { x: seconds, y: obsValues, type: 'bar', name: 'Obstacle Detected' }
      ];
      
      
      Plotly.newPlot('graph-com', data, layout, { displayModeBar: false });
      }
    });
  }
 // Helper function to count the number of points within each second
 function countPoints(data, seconds) {
  var count = Array(seconds.length).fill(0);
  
  for (var i = 0; i < data.length; i++) {
    var time = Math.floor(data[i]);
    var index = seconds.indexOf(time);
    
    if (index !== -1) {
      count[index] += 1;
    }
  }
  
  return count;
}


  function reset(){
    var noData = [];
    Plotly.newPlot('graph-com', noData, layout, { displayModeBar: false });
  }
   // Call updateMap() when the button is clicked
   $('#update-com').click(function() {
    updateMap();
  })
  $('#reset-com').click(function() {
    reset();
  })

  return [updateMap, reset];
}

function initGraphRedundancy() {
  toggleUpdate("redundancy",updateMap);
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
    margin: {
      t: 10, // Top margin
      l: 40, // Left margin
      r: 20, // Right margin
      b: 40  // Bottom margin
    },
    xaxis: { title: 'X Coordinate' },
    yaxis: { title: 'Y Coordinate' }
  };
  Plotly.newPlot('graph-redundancy', data, layout,{ displayModeBar: false });

  function updateMap() {
    $.ajax({
      url: '/get-graph-redundancy',
      type: 'GET',

      success: function(response) {
        var eventData = JSON.parse(response.data);
        console.log(eventData)
        
        var x_car = eventData.x_car;
        var y_car = eventData.y_car;
        var x_obs = eventData.x_obs;
        var y_obs = eventData.y_obs;

        Plotly.update('graph-redundancy', { x: [[x_car], x_obs], y: [[y_car], y_obs]},[0, 1],{ displayModeBar: false });
      }
    });
  }
  function reset(){
    var noData = [];
    Plotly.newPlot('graph-redundancy', noData, layout, { displayModeBar: false });
  }
   // Call updateMap() when the button is clicked
   $('#update-redundancy').click(function() {
    updateMap();
  })
     // Call updateMap() when the button is clicked
    $('#reset-redundancy').click(function() {
     reset();

    })
    return [updateMap, reset];
};

function initGraphNoise() {
    toggleUpdate("obs-raw",updateMap);
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
      margin: {
        t: 10, // Top margin
        l: 40, // Left margin
        r: 20, // Right margin
        b: 40  // Bottom margin
      },
       xaxis: { title: 'X Coordinate' },
       yaxis: { title: 'Y Coordinate' }
     };
 
     Plotly.newPlot('graph-obs-raw', data, layout,{ displayModeBar: false });

     function updateMap() {
      $.ajax({
        url: '/get-graph-obs-raw',
        type: 'GET',
        success: function(response) {
          console.log(response.data);
          var eventData = JSON.parse(response.data);
          
          var x_car = eventData.x_car;
          var y_car = eventData.y_car;
          var x_obs = eventData.x_obs;
          var y_obs = eventData.y_obs;

          Plotly.extendTraces('graph-obs-raw', { x: [[x_car], x_obs], y: [[y_car], y_obs] });
        }
      });
    }
  
  function reset(){
    var noData = [];
    Plotly.newPlot('graph-obs-raw', noData, layout, { displayModeBar: false });
  }
       // Call updateMap() when the button is clicked
   $('#update-obs-raw').click(function() {
    updateMap();
  })
  $('#reset-obs-raw').click(function() {
    reset();
  })
    
     
  return [updateMap, reset];
};

function initKmeanGraph() {
  toggleUpdate("kmeans",updateMap());
  var config = { responsive: true };
  var layout = {
    margin: {
      t: 10, // Top margin
      l: 40, // Left margin
      r: 20, // Right margin
      b: 40  // Bottom margin
    },
    hovermode: 'closest',
    clickmode: 'event+select',
  }; 
 
  var chartData =  { data: [], layout: layout };


  Plotly.newPlot('graph-kmeans', chartData, layout, config,{ displayModeBar: false });
  
  function updateMap() {
    $.ajax({
      url: '/get-graph-kmeans',
      type: 'GET',
      success: function(data) {
         var newChartData = JSON.parse(data);
         Plotly.newPlot('graph-kmeans', newChartData.data, newChartData.layout);
        }
      
    });
  }
  function reset(){
    var noData = [];
    Plotly.newPlot('graph-kmeans', noData, layout, { displayModeBar: false });
  }


  // Call updateMap() at an interval

   // Call updateMap() when the button is clicked
  $('#update-kmeans').click(function() {
    updateMap();
  });
    // Call updateMap() when the button is clicked
   $('#reset-kmeans').click(function() {
    reset();
    });
    return [updateMap, reset];
};


function initKmeanSlider(){
const filterSlider = document.getElementById('filter');
const valueFilter = document.getElementById('valuefilter');

filterSlider.addEventListener('change', function() {
  valueFilter.innerText = this.value;
  updateSliderValues();
});
const max_kSlider = document.getElementById('max_k');
const valuemax_k = document.getElementById('valuemax_k');

max_kSlider.addEventListener('change', function() {
valuemax_k.innerText = this.value;
updateSliderValues();
});
const splitSlider = document.getElementById('split');
const valuesplit = document.getElementById('valuesplit');

splitSlider.addEventListener('change', function() {
valuesplit.innerText = this.value;
updateSliderValues();
});
const thresholdSlider = document.getElementById('threshold');
const valuethreshold = document.getElementById('valuethreshold');

thresholdSlider.addEventListener('change', function() {
valuethreshold.innerText = this.value;
updateSliderValues();
});

function updateSliderValues() {
var filterSlider = $("#filter").val();
var max_kSlider = $("#max_k").val();
var splitSlider = $("#split").val();
var thresholdSlider = $("#threshold").val();

$.ajax({
  url: '/update_kmean_slider',
  type: 'POST',
  data: { filter: filterSlider, max_k: max_kSlider,split:splitSlider,threshold:thresholdSlider },
  success: function(response) {
    console.log('Slider values sent to the server successfully.');
    // Handle the response from the server if needed
  },
  error: function(xhr, status, error) {
    console.error('Error sending slider values to the server:', error);
    // Handle the error if needed
  }
});
}
};

function initMouvement(){
  // Generate an empty 20x20 grid
  var numRows = 20;
  var numCols = 20;
  var data = Array.from({ length: numRows }, () => Array(numCols).fill(null));


  data[2][2] = 0; // Assign a value to represent the grayed-out cell
  data[3][2] = 0; // Assign a value to represent the grayed-out cell
  data[2][3] = 0; // Assign a value to represent the grayed-out cell
  data[3][3] = 0; // Assign a value to represent the grayed-out cell

  // Define the path coordinates
  var pathCoordinates = [
    [0, 1], // Starting cell at row 0, column 1
    [1, 1],  // Ending cell at row 1, column 1
    [1, 2],  // Ending cell at row 1, column 1
    [1, 3],  // Ending cell at row 1, column 1
    [1, 4],  // Ending cell at row 1, column 1
  ];

  // Create the trace for the grid
  var gridTrace = {
    z: data,
    type: 'heatmap',
    colorscale: [[0, 'gray'], [1, 'white']],
    showscale: false
  };

  // Create the trace for the path
  var pathTrace = {
    x: pathCoordinates.map(coord => coord[1]), // Column coordinates
    y: pathCoordinates.map(coord => coord[0]), // Row coordinates
    mode: 'lines',
    line: {
      color: 'red',
      width: 3
    }
  };

  // Create the trace for the markers
  var startTrace = {
    x: [pathCoordinates[0][1]], // Column coordinates of markers
    y: [pathCoordinates[0][0]], // Row coordinates of markers
    mode: 'markers',
    marker: {
      symbol: 'circle',
      size: 10,
      color: 'blue'
    },
    name: 'robot'
  };

  var endTrace = {
    x: [pathCoordinates.at(-1)[1]], // Column coordinates of markers
    y: [pathCoordinates.at(-1)[0]], // Row coordinates of markers
    mode: 'markers',
    marker: {
      symbol: 'circle',
      size: 10,
      color: 'orange'
    },
    name: 'toGo'
  };
  // Define the data array with both traces
  var allData = [gridTrace, pathTrace,startTrace,endTrace];
    // Calculate the endpoint of the vector based on the angle
    var angle = 45; // Replace with your desired angle in degrees
    var angleRad = angle * (Math.PI / 180);
    var vectorX = Math.cos(angleRad);
    var vectorY = Math.sin(angleRad);
  
    // Create the trace for the vector
    var vectorTrace = {
      x: [pathCoordinates[0][1], pathCoordinates[0][1] + vectorX],
      y: [pathCoordinates[0][0], pathCoordinates[0][0] + vectorY],
      mode: 'lines',
      line: {
        color: 'green',
        width: 2
      },
      name: 'vector'
    };
  
    allData.push(vectorTrace); // Add the vector trace to the data array
  

  // Define the layout
  var layout = {
    xaxis: { title: 'Y' },
    yaxis: { title: 'X' },
    margin: {
      t: 10, // Top margin
      l: 40, // Left margin
      r: 20, // Right margin
      b: 40  // Bottom margin
    },
  };

  var graphMovement = document.getElementById('graph-movement');

  // Create the plot
  Plotly.newPlot('graph-movement', allData, layout,{ displayModeBar: false });

  
  var togo = [0,0]
  function updateMap() {
    toggleUpdate("movement",updateMap);

    $.ajax({
      url: '/get-graph-movement',
      type: 'POST',
      data: { togo: JSON.stringify(togo) }, // Send the togo coordinates as data
      success: function(response) {
        var newData = JSON.parse(response.data);
          console.log(newData);

          // Update grid trace
          var numRows = 20;
          var numCols = 20;
          var gridData = Array.from({ length: numRows }, () => Array(numCols).fill(null));
    
          newData.gridData.forEach(function (coord) {
            var row = coord[0];
            var col = coord[1];
            gridData[row][col] = 0;
          });
    
          gridTrace.z = gridData;
    
          // Update path trace
          pathTrace.x = newData.pathX;
          pathTrace.y = newData.pathY;
    
          // Update start trace
          startTrace.x = [newData.pathX[0]];
          startTrace.y = [newData.pathY[0]];
    
          // Update end trace
          endTrace.x = [newData.pathX.at(-1)];
          endTrace.y = [newData.pathY.at(-1)];

          // Update allData array
          allData = [gridTrace, pathTrace, startTrace, endTrace];

              // Calculate the endpoint of the vector based on the angle
          var angle = newData.angle; // Replace with your desired angle in degrees
          var angleRad = angle * (Math.PI / 180);
          var vectorX = Math.cos(angleRad);
          var vectorY = Math.sin(angleRad);
        
          // Create the trace for the vector
          var vectorTrace = {
            x: [pathCoordinates[0][1], pathCoordinates[0][1] + vectorX],
            y: [pathCoordinates[0][0], pathCoordinates[0][0] + vectorY],
            mode: 'lines',
            line: {
              color: 'green',
              width: 2
            },
            name: 'Orientation'
          };
        
          
          allData.push(vectorTrace); // Add the vector trace to the data array
  
                // Redraw the plot
          Plotly.newPlot('graph-movement', allData, layout,{ displayModeBar: false });

          graphMovement.on('plotly_click', handlePlotlyClick);
          
        },
        error: function (error) {
          console.log(error);
        }
    });
  }

  function handlePlotlyClick(eventData) {
            // Retrieve the clicked point's coordinates
            var togoX = eventData.points[0].x;
            var togoY = eventData.points[0].y;

            // Update the togo coordinates
            togo = [togoX, togoY];
            console.log(togo);

            // Call the updateMap() function to update the graph
            updateMap();
  }


  graphMovement.on('plotly_click', handlePlotlyClick);


  function reset(){
    var noData = [];
    Plotly.newPlot('graph-movement', noData, layout, { displayModeBar: false });
  }

 
      // Attach the click event handler to the plot
 
      // Call updateMap() when the button is clicked
  $('#reset-movement').click(function() {
    reset();
  });

      
  $('#update-movement').click(function() {
    updateMap();
  });
    // Call updateMap() when the button is clicked
  $('#reset-movement').click(function() {
    reset();
  });

  return [updateMap, reset];
}


/* --------------- Connection Status Checker --------------- */
$(document).ready(function() {
  initStatusCheck();
});

function initStatusCheck() {
  $.ajax({
    url: "/get-status-value",
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
};

/* --------------- Setting Switch --------------- */
function settingHide(){
  var toggleButton = document.getElementById('toggleButtonHideSetting');
  var settingDivs = document.querySelectorAll('.setting');
  var style = '';
  if (toggleButton.textContent === 'Hide Off') {
    toggleButton.classList.add('active');
    toggleButton.textContent = 'Hide On';
    style = 'none';
  } else {
    toggleButton.textContent = 'Hide Off';
    toggleButton.classList.remove('active');
    style = 'block';
  }
  settingDivs.forEach( function(settingDiv) {
    settingDiv.style.display = style;
  });

 
}
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
$(document).ready(function() {
  initLoggers();
});

function initLoggers(){
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
}




    