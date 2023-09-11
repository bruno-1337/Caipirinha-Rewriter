from ctransformers import AutoModelForCausalLM
import json
# Import the Flask library
from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS
from flask_apscheduler import APScheduler
import time

llm = None
last_request_time = time.time()
#Location of the model
ourmodel = "../../AI/models/converted.bin"
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
    #send the prompt to the model and get the output
    output = llm(prompt)
    #get the number of tokens
    num_tokens = len(output)
    #get the time it took to generate the output
    end_time = time.time()
    # Compute the time elapsed in seconds
    elapsed_time = end_time - start_time
    # Compute the tokens per second
    tokens_per_second = num_tokens / elapsed_time
    #print the output then return it
    print (output)
    #print the tokens per second
    print(f"\n\n#Tokens per second: {tokens_per_second}")
    return output


def load_model():
    #load the model
    print("Loading model...")
    # Use ctransformers to load the model
    global llm
    llm = AutoModelForCausalLM.from_pretrained(ourmodel, model_type=model_type, gpu_layers=gpu_layers, max_new_tokens=max_new_tokens,temperature=temperature,repetition_penalty=repetition_penalty) 
    print("Model loaded!")
    return llm

def unload_model():
    # Unload the model
    global llm
    llm = None
    # Print a message to confirm
    print("Model unloaded!")

def check_and_unload():
    global last_request_time
    global llm
    #get the current time
    current_time = time.time()
    #calculate the difference in seconds
    difference = current_time - last_request_time
    #if the difference is more than 60 seconds, unload the model
    if llm is not None and difference > 180:
        llm = unload_model()


scheduler.add_job(func=check_and_unload, trigger='interval', seconds=60, id='check_and_unload_job')


# Run the app on port 5000 with debug mode on
if __name__ == "__main__":
    scheduler.init_app(app)
    scheduler.start()
    app.run(port=5000, debug=True)
    
    




