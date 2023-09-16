//Default variables

// Settings default values
chrome.storage.sync.get(["ip", "port", "language", "pre_prompt"], function(data) 
{
  if (data.ip == undefined) {
    chrome.storage.sync.set({
      ip: "localhost"
    }, function() {
      console.log("No IP set, using localhost")
    });}

  if (data.port == undefined) {
    chrome.storage.sync.set({
      port: "5000"
    }, function() {
      console.log("No port set, using 5000")
    });}
  if (data.language == undefined) {
    chrome.storage.sync.set({
      language: ""
    }, function() {
      console.log("No language set, using none")
    });}
  if (data.pre_prompt == undefined) {
    chrome.storage.sync.set({
      pre_prompt: "### HUMAN:\nRewrite this with proper grammar and more concise writing style, you will rewrite in the same language as the next message: "
    }, function() 
    {
      console.log("No prompt set, setting default")
    });}
});

// Add a listener to the popup button
chrome.runtime.onMessage.addListener( data => {
	if ( data.type === 'escrevedor_popup_button' ) {
    console.log("CALLED ME HERE!")
		escrevedor( data.message );
	}
  if ( data.type === 'script.js_call' ) {
    console.log("CALLING ESCREVEDOR#$#@$!!!")
    escrevedor( data.message );
    return true;
  }
});

chrome.runtime.onInstalled.addListener( () => {
	chrome.contextMenus.create({
		id: 'escrevedor',
		title: "Escrevedor: %s", 
		contexts:[ "selection" ]
	});
});


// Add a listener to the context menu
chrome.contextMenus.onClicked.addListener( ( info, tab ) => {
	if ( 'escrevedor' === info.menuItemId ) {
    console.log("CALLED ME HERE!!!")
		escrevedor( info.selectionText );
	}
} );




var serverIP = "1234";
var serverPort = "1234";
var Language = "";
var Pre_Prompt = "";
// Function to send a POST request to the LLM
const escrevedor = message => {


  // Get the server IP and port from storage
  chrome.storage.sync.get(["ip", "port", "language", "pre_prompt"], function(data) {
    serverIP = data.ip;
    serverPort = data.port;
    Language = data.language;
    Pre_Prompt = data.pre_prompt;
    console.log(Pre_Prompt)
    console.log("IP: " + serverIP + " PORT: " + serverPort);
  });
  
	if (Language == "") {
    var Post_Prompt = "\n### RESPONSE:\nRewrite: ";
  }
  else{
    var Post_Prompt = "\n### RESPONSE:\nRewrite in "+ Language+": ";
  }
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
    // Send a POST request to the URL
    const HOST = serverIP+":"+serverPort;
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

// Function to inject script.js into the current tab
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

// Add a listener to the keyboard shortcut
chrome.commands.onCommand.addListener((command) => {
  if (command == "Reescrever_Command") {
	injectScript();
  }
  console.log(`Command "${command}" triggered`);
});