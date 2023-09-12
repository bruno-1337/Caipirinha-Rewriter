from ctransformers import AutoModelForCausalLM
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
args = parser.parse_args()
ourmodel = args.model

#setting default variables
llm = None
last_request_time = time.time()
model_type="llama"
#how many gpu_layers to use (run benchmark.py to get optimal value)
gpu_layers=34
#how many tokens to generate
max_new_tokens=256
#temperature of the model
temperature=0.8
#repetition penalty
repetition_penalty=1.1
#how many threads to use (run benchmark.py to get optimal value)
threads=1

besttime=99999
bestlayers=0
rounds_without_improvement=0
prompt = "### HUMAN:\nRewrite this using proper grammar and with a best seller writing style:\n The Kilauea Volcano in Hawaii, one of the world's most active volcanoes, has started erupting, unleashing lava fountains inside its crater.\n###RESPONSE:\nRewrite:"

def benchmark_gpu_layers(layers):
    #model type
    #how many gpu_layers to use
    global gpu_layers
    global besttime
    global bestlayers
    global rounds_without_improvement
    gpu_layers=layers + 1
    global prompt
    timer = time.time()
    try:
        print(f"\nNext test! Trying to load model with {gpu_layers} layers")
        load_model()
        gettingAlpaca(prompt)
        unload_model()
    except RuntimeError:
        print("Oops! your GPU cant handle that much layers")
        unload_model()
        print(besttime)
        print(bestlayers)
        return gpu_layers
    timetook = time.time() - timer
    if timetook < besttime:
        besttime = timetook
        bestlayers=gpu_layers
        rounds_without_improvement=0
        print(f"####New best time so far: {besttime}")
        print(f"####New best layers so far: {bestlayers}")
    else:
        rounds_without_improvement += 1
    print(f"Time taken for this run: {timetook}")
    print(f"Best time so far: {besttime}")
    print(f"Best layers so far: {bestlayers}")
    print(f"Rounds without improvement: {rounds_without_improvement}")
    if rounds_without_improvement > 10:
        return gpu_layers
    benchmark_gpu_layers(gpu_layers)

def benchmark_threads(howmanythreads):
    #model type
    #how many threads to use
    global threads
    global besttime
    global bestlayers
    global rounds_without_improvement
    threads=howmanythreads + 1
    global prompt
    timer = time.time()
    try:
        print(f"\nNext test! Trying to load model with {threads} threads")
        load_model()
        gettingAlpaca(prompt)
        unload_model()
    except RuntimeError:
        print("Oops! We cant handle that much threads")
        unload_model()
        print(besttime)
        print(bestlayers)
        return threads
    timetook = time.time() - timer
    if timetook < besttime:
        besttime = timetook
        bestlayers=threads
        rounds_without_improvement=0
        print(f"####New best time so far: {besttime}")
        print(f"####New best thread number so far: {bestlayers}")
    else:
        rounds_without_improvement += 1
    print(f"Time taken for this run: {timetook}")
    print(f"Best time so far: {besttime}")
    print(f"Best thread number so far: {bestlayers}")
    print(f"Rounds without improvement: {rounds_without_improvement}")
    if rounds_without_improvement > 10:
        return threads
    benchmark_threads(threads)

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
    global llm
    llm = AutoModelForCausalLM.from_pretrained(ourmodel, model_type=model_type, gpu_layers=gpu_layers,seed=5,threads=threads, max_new_tokens=max_new_tokens,temperature=temperature,repetition_penalty=repetition_penalty) 
    print("Model loaded!")
    print(f"Time taken to load model: {time.time() - timer}")
    return llm

def unload_model():
    # Unload the model
    global llm
    llm = None
    print("Model unloaded!")

selector = input("Select benchmark option (First run GPU Layers, then Threads):\n1. Benchmark GPU layers\n2. Benchmark threads\n3. Exit\n")
if selector == "1":
    print("Benchmarking GPU layers")
    threads = int(input("How many threads do you want to use?\n"))
    gpu_layers = 1
    benchmark_gpu_layers(gpu_layers)
if selector == "2":
    gpu_layers = int(input("How many GPU layers do you want to use? (Run GPU Layers benchmark for optimal performance\n"))
    print("Benchmarking threads")
    benchmark_threads(1)