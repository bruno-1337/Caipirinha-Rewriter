/* Get the current prompt from storage and display it
chrome.storage.sync.get("prompt", function(data) {
  document.getElementById("current-prompt").textContent = data.prompt;
});*/

// Get the server IP and port from storage and fill in the input fields
chrome.storage.sync.get(["ip", "port", "language", "pre_prompt", "shortcut"], function(data) 
{
  document.getElementById("server-ip").value = data.ip;
  document.getElementById("server-port").value = data.port;
  document.getElementById("language").value = data.language;
  document.getElementById("new-prompt").value = data.pre_prompt;
});


// Add a click event listener to the save button
document.getElementById("save-button").addEventListener("click", function() {
  var newPrompt = document.getElementById("new-prompt").value;
  var serverIp = document.getElementById("server-ip").value;
  var serverPort = document.getElementById("server-port").value;
  var languageUsed = document.getElementById("language").value;
  // Validate the input values
  if (newPrompt) {
    // Save the new prompt to storage
    chrome.storage.sync.set({
      pre_prompt: newPrompt
    }, function() {
      // Display a confirmation message
      console.log("Saved the new prompt!")
    });}

  if (serverIp) {
    // Save the new server IP to storage
    chrome.storage.sync.set({
      ip: serverIp
    }, function() {
      console.log("Saved the new IP!")
    });}
    if (language) {
      // Save the new server language to storage
      chrome.storage.sync.set({
        language: languageUsed
      }, function() {
        console.log("Saved the new language!")
      });}

  if (serverPort) {
    // Save the new server port to storage
    chrome.storage.sync.set({
      port: serverPort
    }, function() {
      console.log("Options the new Port!")
    });
  
  } else {
    // Display an error message
    alert("Please enter valid values!");
    console.log("Please enter valid values!")
  }
  alert("Saved the new settings!!")
});
