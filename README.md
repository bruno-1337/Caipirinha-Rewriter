# Text-Generation-WebUI Chrome Extension

This is a chrome extension that allows you to interact with the [text-generation-webui] API to have self hosted AI writing tools integrated on your browser. You can use this extension to generate text for various purposes, such as writing essays, stories, poems, code, and more.

## Features

- Highlight any text on a web page and press CTRL+D to send it as a prompt to the text-generation-webui API. The generated text will be copied to your clipboard and printed on the console.
- Customize the parameters of the text-generation-webui API, such as length, temperature, top_p, and frequency_penalty.
- Choose from different models and languages supported by the text-generation-webui API.

## Installation

To install this extension, follow these steps:

1. Clone or download this repository to your local machine.
2. Go to chrome://extensions/ and enable developer mode.
3. Click on "Load unpacked" and select the folder where you cloned or downloaded this repository.
4. You should see the extension icon on your browser toolbar.

## Usage

To use this extension, you need to have the text-generation-webui API running on your local machine or a remote server. You can find the instructions on how to set up the text-generation-webui API [here].

Once you have the text-generation-webui API running, you need to configure the extension settings. To do this, click on the extension icon and go to "Options". There, you can enter the URL of the text-generation-webui API endpoint, such as http://localhost:5000 or http://your-server.com:5000. You can also adjust the parameters of the text-generation-webui API, such as length, temperature, top_p, and frequency_penalty. You can also select the model and language you want to use.

After you have configured the extension settings, you can start using it on any web page. To generate text from a prompt, simply highlight any text on a web page and press CTRL+D. The generated text will be copied to your clipboard and printed on the console. You can paste it anywhere you want.

## Issues

This is my first chrome extension, so it may have some bugs or limitations. Some of the known issues are:

- The extension only works with plain text prompts. It does not support markdown or other formatting options.
- The extension does not have a user interface to display the generated text. It only copies it to the clipboard and prints it on the console.
- The extension does not have a way to cancel or stop the text generation process once it is started.
- The extension does not have a way to save or export the generated text.

If you encounter any other issues or have any suggestions for improvement, please feel free to open an issue or a pull request on this repository.

## License

This project is licensed under the GNU Affero General Public License - see the [LICENSE] file for details.
