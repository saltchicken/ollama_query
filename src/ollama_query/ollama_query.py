import requests
import time

def ollama_query(model, prompt, system_message=None, host="localhost", port=11434):
    """ 
    Query the ollama API with a prompt and return the response. 

    PARAMS:
        model: The name of the model to use.
        prompt: The prompt to send to the model.
        system_message: The system message to send to the model.
        host: The host to send the request to.
        port: The port to send the request to.
    RETURNS:
        The response from the model.
        Debug text
    """
    url = f"http://{host}:{port}/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    if system_message:
        data["system"] = system_message
    # TODO: How can I get the default system message?
    start_time = time.perf_counter()
    result = requests.post(url, headers=headers, json=data)
    print(result)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    result = result.json()

    input_tokens = result.get("prompt_tokens", 0)
    output_tokens = result.get("eval_tokens", 0)
    response = result.get("response", None)

    debug_string = evaluate_debug_string(prompt, system_message, response, elapsed_time, input_tokens, output_tokens)
    return response, debug_string

def evaluate_debug_string(prompt, system_message, response, elapsed_time, input_tokens, output_tokens):
    """ 
    Evaluate the debug string for the ollama query. 

    PARAMS:
        prompt: The prompt that was sent to the model.
        system_message: The system message that was sent to the model.
        response: The response from the model.
        elapsed_time: The elapsed time for the query.
        input_tokens: The number of input tokens.
        output_tokens: The number of output tokens.
    RETURNS:
        The debug string.
    """
    tokens_per_second = output_tokens / elapsed_time if elapsed_time > 0 else 0
    debug_string = f"""
--------STATS--------
Input tokens: {input_tokens}
Tokens per second: {tokens_per_second:.2f}
Elapsed time: {elapsed_time:.2f} seconds
-------SYSTEM MESSAGE--------
{system_message}
----------PROMPT---------
{prompt}
----------RESPONSE---------
{response}
"""
    return debug_string
