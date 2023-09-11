console.log("script.js loaded")

function getText() {
    // Use window.getSelection to get the selected text
    var text = window.getSelection().toString();
    // Check if the text is not empty
    if (text) {
      // Return the text
        return text;
    }
    else {
        console.log("No text selected")
        return "No text selected";
    }
}

// Get the output of your function
var output = getText();
// Send a message to background.js with the output as data
chrome.runtime.sendMessage({type: 'script.js_call', message: output}, function(response) {
  // Do something with the response from background.js, if needed
  console.log("enviei pro background");
    // Copy the result to the clipboard
});




function copyTextToClipboard(text) {
    // Create a textarea element where we can insert text to
    var copyFrom = document.createElement("textarea");
    // Set the text content to be the text parameter
    copyFrom.textContent = text;
    // Append the textarea element to the body
    document.body.appendChild(copyFrom);
    



    // Select the textarea element
    copyFrom.select();
    // Execute the copy command
    console.log("copiei esse texto: " + text);
    document.execCommand("copy");
    // Remove the textarea element from the body
    document.body.removeChild(copyFrom);
  }


  chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
      // Check if the message is to call the returning_text function
      if (request.message === "returning_text") {
        // Call the copyTextToClipboard with the data recieved from the LLM
        copyTextToClipboard(request.text);
      }
    }
  );