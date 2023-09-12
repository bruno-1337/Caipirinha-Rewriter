# [Caipirinha Rewriter](https://github.com/bruno-1337/Caipirinha-Rewriter/) 🍹

This is a Chrome extension that integrates an AI-powered writing tool into your browser, allowing you to interact with a self-hosted LLM model for rewriting text. With this extension, you can rewrite text for various purposes, such as essays, stories, poems, code, and more.

## Features

- Highlight any text on a web page and press CTRL+D to send it as a prompt to the server. The generated text will be copied to your clipboard and printed on the console.
- Customize the parameters, such as length, temperature, top_p, and frequency_penalty.
- Choose from different models.

## Installation

To install this extension, follow these steps:

1. Clone or download this repository to your local machine.
2. Go to chrome://extensions/ and enable developer mode.
3. Click on "Load unpacked" and select the folder where you cloned or downloaded this repository.
4. You should see the extension icon on your browser toolbar.

To use this extension, you need to have [CTransformers](https://github.com/marella/ctransformers) installed. You can easily install it with
```sh
pip install ctransformers
```
for GPU support you will also need:

Nvidia users [CUDA support]
```sh
pip install ctransformers[cuda]
```
AMD users [ROCm support]
```sh
CT_HIPBLAS=1 pip install ctransformers --no-binary ctransformers
```
Apple users [Metal support]
```sh
CT_METAL=1 pip install ctransformers --no-binary ctransformers
```


## Usage
After that you can start the server with
```sh
python server.py -p -model -threads -gpu_layers -batch_size
```
Options:
```sh
  [-h], [--help]       show this help message and exit
  [-m], [-model]       model to use
  [-p], [-port]        port the server will use
  [-t], [-threads]     threads to use
  [-g], [-gpu_layers]  gpu layers to use
  [-b], [-batch_size]  batch size to use 
```
if you dont know what values to use, you can use benchmark.py to see what gets you the best performance for your pc

After starting the server, open your browser and navigate to the options of the extension. 
Enter the IP address (use "localhost" if local) and port number and save, then set the hotkey on your browser
After that you can go on any webpage and highlight a text, when you press the hotkey it will send the prompt to the server. This is the default prompt:
```sh
	### HUMAN:
  Rewrite this with proper grammar and more concise writing style: [HIGHLIGHTED_TEXT]";
	### RESPONSE:
  Rewrite: ";
```
Currently, I have tested the application using [Llama2-7b-chat-uncensored](https://huggingface.co/TheBloke/llama2_7b_chat_uncensored-GGML)

## Issues

This is my first chrome extension, so it may have some bugs or limitations. Some of the known issues are:

- The extension does not have a user interface to display the generated text. It only copies it to the clipboard and prints it on the console.
- The extension does not have a way to cancel or stop the text generation process once it is started.
- The extension does not have a way to save or export the generated text.

If you encounter any other issues or have any suggestions for improvement, please feel free to open an issue or a pull request on this repository.

## License

This project is licensed under the GNU Affero General Public License - see the [LICENSE] file for details.
