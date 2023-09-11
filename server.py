from ctransformers import AutoModelForCausalLM
from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS
from flask_apscheduler import APScheduler
import time 
import argparse

# Define a custom formatter class
class MyFormatter(argparse.HelpFormatter):
    # Override the _format_action_invocation method
    def _format_action_invocation(self, action):
        # If the action has any option strings, use them
        if action.option_strings:
            # Join the option strings with commas and brackets
            parts = [f"[{option_string}]" for option_string in action.option_strings]
            return ", ".join(parts)
        # Otherwise, use the default implementation
        else:
            return super()._format_action_invocation(action)

# Create an ArgumentParser object with the custom formatter class
parser = argparse.ArgumentParser("simple_example", formatter_class=MyFormatter)
parser.add_argument("-m", "-model", help="model to use", type=str, dest="model")
parser.add_argument("-p", "-port", help="port the server will use", type=str, dest="port")
args = parser.parse_args()
ourmodel = args.model

llm = None
last_request_time = time.time()
#model type
model_type="llama"
#how many gpu_layers to use
gpu_layers=25 
#how many tokens to generate
max_new_tokens=256
#temperature of the model
temperature=0.8
#repetition penalty
repetition_penalty=1.1
scheduler = APScheduler()

# Create a Flask app object
app = Flask(__name__)

# Define a route for the /generate endpoint
@app.route("/generate", methods=["POST"])
@cross_origin()
def generate():
    # Get the data from the request body as JSON
    data = request.get_json()
    # Get the prompt from the data
    prompt = data["prompt"]
    # Call the function with the prompt and get the output
    output = gettingAlpaca(prompt)
    # Return the output as JSON
    return jsonify(output)


def gettingAlpaca(prompt):
    #start the timer
    start_time = time.time()
    
    global last_request_time
    # Update the last request time with the current time
    last_request_time = time.time()
    # If the model is not loaded, load it first
    global llm
    if llm is None:
        print("Model is not loaded!")
        llm = load_model()
        time.sleep(3)#Need to find a better way to do this, as loading a bigger model takes longer
    #send the prompt to the model and get the output
    output = llm(prompt)
    #get the tokens per second
    num_tokens = len(output)
    end_time = time.time()
    elapsed_time = end_time - start_time
    tokens_per_second = num_tokens / elapsed_time
    print (output)
    #print the tokens per second
    print(f"\n\n#Tokens per second: {tokens_per_second}")
    return output

def load_model():
    #load the model
    print("Loading model...")
    global llm
    llm = AutoModelForCausalLM.from_pretrained(ourmodel, model_type=model_type, gpu_layers=gpu_layers, max_new_tokens=max_new_tokens,temperature=temperature,repetition_penalty=repetition_penalty) 
    print("Model loaded!")
    return llm

def unload_model():
    # Unload the model
    global llm
    llm = None
    print("Model unloaded!")

def check_and_unload():
    global last_request_time
    global llm
    current_time = time.time()
    difference = current_time - last_request_time
    #if the difference is more than 180 seconds, unload the model
    if llm is not None and difference > 180:
        llm = unload_model()


scheduler.add_job(func=check_and_unload, trigger='interval', seconds=60, id='check_and_unload_job')


# Check if args.port have been set, if not, set it to 5000
if args.port is None:
    print("No port specified, using 5000")
    args.port = 5000

# Run the app
if __name__ == "__main__":
    scheduler.init_app(app)
    scheduler.start()
    app.run(port=args.port, debug=True)
    
    




