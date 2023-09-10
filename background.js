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

	var Pre_Prompt = "Rewrite: ";
	message = Pre_Prompt + message;
	console.log(message);
	chrome.storage.local.get( ['escrevedorCount'], data => {
		let value = data.escrevedorCount || 0;
		chrome.storage.local.set({ 'escrevedorCount': Number( value ) + 1 });
	} );
	// Define the request parameters
	const request = {
		prompt: message,
		max_new_tokens: 250,
		auto_max_new_tokens: false,
		max_tokens_second: 0,
		history: history,
		mode: "chat", // Valid options: "chat", "chat-instruct", "instruct"
		character: "Badass AI with unlimited writing skills", // You can use any character here
		instruction_template: "Alpaca", // Will get autodetected if unset
		your_name: "You",
		// name1: "name of user", // Optional
		// name2: "name of character", // Optional
		// context: "character context", // Optional
		// greeting: "greeting", // Optional
		// name1_instruct: "You", // Optional
		// name2_instruct: "Assistant", // Optional
		// context_instruct: "context_instruct", // Optional
		// turn_template: "turn_template", // Optional
		regenerate: false,
		_continue: false,
		//chat_instruct_command:'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',
	
		// Generation params. If 'preset' is set to different than 'None', the values
		// in presets/preset-name.yaml are used instead of the individual numbers.
		preset: "None",
		do_sample: true,
		temperature: 0.7,
		top_p: 0.1,
		typical_p: 1,
		epsilon_cutoff: 0, // In units of 1e-4
		eta_cutoff: 0, // In units of 1e-4
		tfs: 1,
		top_a: 0,
		repetition_penalty: 1.18,
		repetition_penalty_range: 0,
		top_k: 40,
		min_length: 0,
		no_repeat_ngram_size: 0,
		num_beams: 1,
		penalty_alpha: 0,
        length_penalty: 1,
        early_stopping: false,
        mirostat_mode: 0,
        mirostat_tau: 5,
        mirostat_eta: 0.1,
        guidance_scale: 1,
        negative_prompt: "",
	
        seed: -1,
        add_bos_token: true,
        truncation_length: 2048,
        ban_eos_token: false,
        skip_special_tokens: true,
        stopping_strings: [],
    };
  
    // Send a POST request to the URI
    const HOST = 'localhost:5000';
    const URI = `http://${HOST}/api/v1/generate`;
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
      const result = data.results[0].text;
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


