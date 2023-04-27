function callPythonFunction(sliderValue) {
  $.ajax({
    url: "/run-python-function",
    type: "POST",
    data: { value: sliderValue },
    success: function(response) {
      //console.log(response);
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
