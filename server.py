from ctransformers import AutoModelForCausalLM
from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS
from flask_apscheduler import APScheduler
import time 
import argparse

# Argument Parser
class MyFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if action.option_strings:
            parts = [f"[{option_string}]" for option_string in action.option_strings]
            return ", ".join(parts)
        else:
            return super()._format_action_invocation(action)
parser = argparse.ArgumentParser("simple_example", formatter_class=MyFormatter)
parser.add_argument("-m", "-model", help="model to use", type=str, dest="model")
parser.add_argument("-p", "-port", help="port the server will use", type=str, dest="port")
parser.add_argument("-t", "-threads", help="threads to use", type=int, dest="threads")
parser.add_argument("-g", "-gpu_layers", help="gpu layers to use", type=int, dest="gpu_layers")
parser.add_argument("-b", "-batch_size", help="batch size to use", type=int, dest="batch_size")



args = parser.parse_args()


# Load from arguments
ourmodel = args.model
batch_size = args.batch_size
gpu_layers = args.gpu_layers
threads = args.threads

#setting default variables
llm = None
last_request_time = time.time()
model_type="llama"
if gpu_layers is None:
    print("No gpu layers specified, using 1")
    gpu_layers = 1
if batch_size is None:
    print("No batch size specified, using 8")
    batch_size = 8
if threads is None:
    print("No threads specified, using 0")
    threads = 0
max_new_tokens=256
temperature=0.8
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
    global llm
    if llm is None:
        print("Model is not loaded!")
        llm = load_model()
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
    timer = time.time()
    print("Loading model...")
    print("#Using {} threads".format(threads))
    print("#Using {} gpu layers".format(gpu_layers))
    print("#Using {} batch size".format(batch_size))
    global llm
    llm = AutoModelForCausalLM.from_pretrained(ourmodel, model_type=model_type,threads=threads,batch_size=batch_size, gpu_layers=gpu_layers, max_new_tokens=max_new_tokens,temperature=temperature,repetition_penalty=repetition_penalty) 
    print("Model loaded!")
    print(f"Time taken to load model: {time.time() - timer}")
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

#add the job to the scheduler
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
    
    




