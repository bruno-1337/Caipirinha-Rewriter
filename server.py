from ctransformers import AutoModelForCausalLM
import json
# Import the Flask library
from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS

#import time to get tokens per second
import time

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
    #send the prompt to the model
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

#load the model
print("Loading model...")
# Use ctransformers to load the model
llm = AutoModelForCausalLM.from_pretrained(ourmodel, model_type=model_type, gpu_layers=gpu_layers, max_new_tokens=max_new_tokens,temperature=temperature,repetition_penalty=repetition_penalty) 
print("Model loaded!")





# Run the app on port 5000 with debug mode on
if __name__ == "__main__":
    app.run(port=5000, debug=True)
