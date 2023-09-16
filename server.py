# Import the required modules
from ctransformers import AutoModelForCausalLM
from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS
from flask_apscheduler import APScheduler
import time 
import argparse

# Define some constants
MODEL_TYPE = "llama"
MAX_NEW_TOKENS = 256
TEMPERATURE = 0.8
REPETITION_PENALTY = 1.1
TIMEOUT = 120 # seconds to unload the model if no requests

# Create a custom formatter for the argument parser
class MyFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if action.option_strings:
            parts = [f"[{option_string}]" for option_string in action.option_strings]
            return ", ".join(parts)
        else:
            return super()._format_action_invocation(action)

# Parse the arguments from the command line
parser = argparse.ArgumentParser("simple_example", formatter_class=MyFormatter)
parser.add_argument("-m", "-model", help="model to use", type=str, dest="model", required=True)
parser.add_argument("-p", "-port", help="port the server will use", type=str, dest="port", default=5000)
parser.add_argument("-t", "-threads", help="threads to use", type=int, dest="threads", default=0)
parser.add_argument("-g", "-gpu_layers", help="gpu layers to use", type=int, dest="gpu_layers", default=1)
parser.add_argument("-b", "-batch_size", help="batch size to use", type=int, dest="batch_size", default=8)

args = parser.parse_args()

# Initialize some global variables
llm = None # the model object
last_request_time = time.time() # the last time a request was made

# Create a Flask app object and a scheduler object
app = Flask(__name__)
scheduler = APScheduler()

# Import threading module
import threading

# Create a global lock object
lock = threading.Lock()

# Define a decorator function that checks the lock status
def check_lock(func):
    def wrapper(*args, **kwargs):
        # Try to acquire the lock
        if lock.acquire(blocking=False):
            # If successful, execute the original function
            try:
                return func(*args, **kwargs)
            finally:
                # Release the lock after finishing
                lock.release()
                print("Lock released!")
        else:
            # If not successful, return an error message
            return jsonify({"error": "Server is busy, please try again later"})
    return wrapper

# Use the decorator on your route functions
@app.route("/generate", methods=["POST"])
@cross_origin()
@check_lock
def generate():
    # Your original code here

    # Get the data from the request body as JSON
    data = request.get_json()
    # Get the prompt from the data
    prompt = data["prompt"]
    # Load the model if it is not loaded yet
    global llm
    if llm is None:
        print("Model is not loaded!")
        llm = load_model()
    # Update the last request time with the current time
    global last_request_time
    last_request_time = time.time()
    # Call the function with the prompt and get the output
    output = generate_text(prompt)
    # Return the output as JSON
    return jsonify(output)

def generate_text(prompt):
    # Start the timer
    start_time = time.time()
    # Generate the text using the model and the prompt
    output = llm(prompt)
    # Get the number of tokens and the elapsed time
    num_tokens = len(output)
    end_time = time.time()
    elapsed_time = end_time - start_time
    # Calculate and print the tokens per second
    tokens_per_second = num_tokens / elapsed_time
    print (output)
    print(f"\n\n#Tokens per second: {tokens_per_second}")
    # Return the output text
    return output

def load_model():
    # Start the timer
    timer = time.time()
    # Print some information about the model parameters
    print("Loading model...")
    print(f"#Using {args.threads} threads")
    print(f"#Using {args.gpu_layers} gpu layers")
    print(f"#Using {args.batch_size} batch size")
    # Load and return the model object using the arguments
    global llm
    llm = AutoModelForCausalLM.from_pretrained(args.model, model_type=MODEL_TYPE, threads=args.threads, batch_size=args.batch_size, gpu_layers=args.gpu_layers, max_new_tokens=MAX_NEW_TOKENS, temperature=TEMPERATURE, repetition_penalty=REPETITION_PENALTY) 
    # Print some information about the loading time 
    print("Model loaded!")
    print(f"Time taken to load model: {time.time() - timer}")
    return llm

def unload_model():
    # Unload and delete the model object
    global llm
    del llm 
    llm = None
    
    # Print a message to indicate that the model is unloaded
    print("Model unloaded!")

def check_and_unload():
    
     # Check if there is a model object and if it has been idle for more than TIMEOUT seconds 
     global last_request_time 
     global llm 
     current_time = time.time() 
     difference = current_time - last_request_time 
     if llm is not None and difference > TIMEOUT: 
         # Unload the model object 
         unload_model()

# Add the job to the scheduler to check and unload the model every 60 seconds
scheduler.add_job(func=check_and_unload, trigger='interval', seconds=60, id='check_and_unload_job')

# Run the app
if __name__ == "__main__":
    scheduler.init_app(app)
    scheduler.start()
    app.run(host="0.0.0.0", port=args.port, debug=True)
