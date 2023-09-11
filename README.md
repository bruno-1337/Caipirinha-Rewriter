# Caipirinha Rewriter: Spice up your text with your own self-hosted AI

This is a Chrome extension that integrates an AI-powered writing tool into your browser, allowing you to interact with a self-hosted LLM model for rewriting text. With this extension, you can rewrite text for various purposes, such as essays, stories, poems, code, and more.

## Features

- Highlight any text on a web page and press CTRL+D to send it as a prompt to the text-generation-webui API. The generated text will be copied to your clipboard and printed on the console.
- Customize the parameters, such as length, temperature, top_p, and frequency_penalty.
- Choose from different models.

## Installation

To install this extension, follow these steps:

1. Clone or download this repository to your local machine.
2. Go to chrome://extensions/ and enable developer mode.
3. Click on "Load unpacked" and select the folder where you cloned or downloaded this repository.
4. You should see the extension icon on your browser toolbar.

## Usage

To use this extension, you need to have [CTransformers](https://github.com/marella/ctransformers) installed. You can easily install it with
```sh
pip install ctransformers
```
After that you can start the server with
```sh
python server.py -p [what port to open the server] -model [what model to load]
```
if not specified will use port 5000

After starting the server, open your browser and navigate to the options of the extension. 
Enter the IP address (use "localhost" if local) and port number and save

After that you can go on any webpage and highlight a text, when you press CTRL+D it will send the text to the server with the prompt:
```sh
	### HUMAN:
  Rewrite this with proper grammar and more concise writing style: [HIGHLIGHTED_TEXT]";
	### RESPONSE:
  Rewrite: ";
```
Currently, I have tested the application only on [Llama2-7b-chat-uncensored](https://huggingface.co/TheBloke/llama2_7b_chat_uncensored-GGML)

## Issues

This is my first chrome extension, so it may have some bugs or limitations. Some of the known issues are:

- The extension does not have a user interface to display the generated text. It only copies it to the clipboard and prints it on the console.
- The extension does not have a way to cancel or stop the text generation process once it is started.
- The extension does not have a way to save or export the generated text.

If you encounter any other issues or have any suggestions for improvement, please feel free to open an issue or a pull request on this repository.

## License

This project is licensed under the GNU Affero General Public License - see the [LICENSE] file for details.
