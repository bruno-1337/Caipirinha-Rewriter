const text = document.getElementById( 'escrevedor-text' );
const save_new_prompt = document.getElementById( 'save_new_prompt_button' );
const current_prompt = document.getElementById( 'current_prompt' );
const new_prompt = document.getElementById( 'new-prompt' );



// Get the current prompt and count from storage and display them
chrome.storage.sync.get(["pre_prompt"], function(data) 
{
	//let prompt = data.pre_prompt || "No prompt set";
	//current_prompt.innerHTML = prompt;
	document.getElementById("new-prompt").value = data.pre_prompt;
});

// Add a listener to the storage change event
chrome.storage.onChanged.addListener( ( changes, namespace ) => {
	if ( changes.escrevedorCount ) {
		let value = changes.escrevedorCount.newValue || 0;
		counter.innerHTML = value;
	}
});
// Add a click event listener to the save button
save_new_prompt.addEventListener( 'click', () => 
{
	var newPrompt = document.getElementById("new-prompt").value;
	chrome.storage.sync.set({
		pre_prompt: newPrompt
	  }, function() {
		// Display a confirmation message
		console.log("Saved the new prompt!")
	  });}
 );
// Go to options button
document.querySelector('#go-to-options').addEventListener('click', function() {
	if (chrome.runtime.openOptionsPage) {
	  chrome.runtime.openOptionsPage();
	} else {
	  window.open(chrome.runtime.getURL('options.html'));
	}
  });


chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	// Check if the message is to call our function
	if (request.action === 'callMyFunction') {
	  // Get the selected text
	  let selectedText = window.getSelection().toString();
	  // Call our function with the selected text as an argument
	  let result = myFunction(selectedText);
	  // Send a message to the background script with the result
	  chrome.runtime.sendMessage({action: 'myFunctionResult', result: result});
	}
  });

  function myFunction(text) {
	// Do something with the text and return a value
	return text.toUpperCase();
  }

