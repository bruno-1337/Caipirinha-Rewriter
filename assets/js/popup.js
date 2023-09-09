const text = document.getElementById( 'escrevedor-text' );
const escrevedor = document.getElementById( 'escrevedor-button' );
const reset = document.getElementById( 'escrevedor-reset' );
const counter = document.getElementById( 'escrevedor-count' );

chrome.storage.local.get( ['escrevedorCount'], data => {
	let value = data.escrevedorCount || 0;
	counter.innerHTML = value;
} );

chrome.storage.onChanged.addListener( ( changes, namespace ) => {
	if ( changes.escrevedorCount ) {
		let value = changes.escrevedorCount.newValue || 0;
		counter.innerHTML = value;
	}
});

reset.addEventListener( 'click', () => {
	chrome.storage.local.clear();
	text.value = '';
} );

escrevedor.addEventListener( 'click', () => {
	chrome.runtime.sendMessage( '', {
		type: 'notification',
		message: text.value
	});
} );

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

