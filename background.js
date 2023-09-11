chrome.runtime.onMessage.addListener( data => {
	if ( data.type === 'notification' ) {
		escrevedor( data.message );
	}
});

chrome.runtime.onInstalled.addListener( () => {
	chrome.contextMenus.create({
		id: 'escrevedor',
		title: "Escrevedor: %s", 
		contexts:[ "selection" ]
	});
});

let history = { internal: [], visible: [] };

chrome.contextMenus.onClicked.addListener( ( info, tab ) => {
	if ( 'escrevedor' === info.menuItemId ) {
		escrevedor( info.selectionText );
	}
} );
const escrevedor = message => {

	var Pre_Prompt = "### HUMAN:\nRewrite this with proper grammar and more concise writing style: ";
	var Post_Prompt = "\n### RESPONSE:\nRewrite: ";
	message = Pre_Prompt + message + Post_Prompt;
	console.log(message);
	chrome.storage.local.get( ['escrevedorCount'], data => {
		let value = data.escrevedorCount || 0;
		chrome.storage.local.set({ 'escrevedorCount': Number( value ) + 1 });
	} );
	// Define the request parameters
	const request = {
		prompt: message
    };
  
    // Send a POST request to the URI
    const HOST = 'localhost:5000';
    const URI = `http://${HOST}/generate`;
    fetch(URI, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request)
    })
    .then(response => {
      // Check the status code
      if (response.status === 200) {
        // Parse the JSON response
        console.log("200!!!");
        //return response.json();
        return response.json();
      } else {
        // Throw an error
        console.log(`Request failed with status code ${response.status}`);
        throw new Error(`Request failed with status code ${response.status}`);
      }
    })
    .then(data => {
      // Get the result text from the data
      const result = data
      // Print the prompt and the result
      console.log("We recieves this from the LLM:" + result);
      if (result) {
        //now we send the result to the content script by calling returning_text
            chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
              var activeTab = tabs[0];
              chrome.tabs.sendMessage(activeTab.id, {"message": "returning_text", "text": result});
            });
      }
    })
    .catch(error => {
      // Handle the error
      console.error(error);
    });
};




chrome.commands.onCommand.addListener((command) => {
  if (command == "Reescrever_Command") {
	// Get the selected text
	injectScript();
	//getText();
	// Call our function with the selected text as an argument
  }
  console.log(`Command "${command}" triggered`);
});

function injectScript() {
	// Get the current tab ID
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
	  let tabId = tabs[0].id;
	  // Execute script.js in the main frame of the tab
	  chrome.scripting.executeScript({
		target: {tabId: tabId},
		files: ["assets/js/script.js"]
	  }).then(() => console.log("script injected"));
	});
  }


// Listen for messages from script.js
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
	// Get the data from the message
	var data = message.data;
	// Do something with the data, such as calling another function
	console.log("Got this data: " + data);
	//Send data to escrevedor
	resultado = escrevedor(data);
	// Send a response
	sendResponse({result: null});
});


