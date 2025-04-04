import requests

def ollama_query(model, prompt, system_message=None, host="localhost", port=11434, temperature=None, seed=None):
    """ 
    Query the ollama API with a prompt and return the response. 

    PARAMS:
        model: The name of the model to use.
        prompt: The prompt to send to the model.
        system_message: The system message to send to the model.
        host: The host to send the request to.
        port: The port to send the request to.
        temperature: Controls randomness of the model. Lower values will make the model more deterministic. Range: 0 to 1. Defaults to settings from Modelfile.
        seed: Optional seed for deterministic results.
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
    if temperature:
        data["temperature"] = temperature
    if seed:
        data["seed"] = seed
    # TODO: How can I get the default system message?
    result = requests.post(url, headers=headers, json=data)
    # print(result)
    result = result.json()

    response = result.get("response", None)

    input_tokens = result.get("prompt_eval_count", 0)
    output_tokens = result.get("eval_count", 0)

    total_duration = result.get("total_duration", 0)
    load_duration = result.get("load_duration", 0)
    prompt_eval_duration = result.get("prompt_eval_duration", 0)
    eval_duration = result.get("eval_duration", 0)

    debug_string = evaluate_debug_string(prompt, system_message, response, total_duration, input_tokens, output_tokens, eval_duration)
    return response, debug_string

def evaluate_debug_string(prompt, system_message, response, total_duration, input_tokens, output_tokens, eval_duration):
    """ 
    Evaluate the debug string for the ollama query. 

    PARAMS:
        prompt: The prompt that was sent to the model.
        system_message: The system message that was sent to the model.
        response: The response from the model.
        total_duration: The elapsed time for the query.
        input_tokens: The number of input tokens.
        output_tokens: The number of output tokens.
        eval_duration: The elapsed time for the model to generate the response.
    RETURNS:
        The debug string.
    """
    total_duration = total_duration / 1_000_000_000
    eval_duration = eval_duration / 1_000_000_000
    tokens_per_second = output_tokens / eval_duration if eval_duration > 0 else 0
    debug_string = f"""
--------STATS--------
Input tokens: {input_tokens}
Tokens per second: {tokens_per_second:.2f}
Total duration: {total_duration:.2f} seconds
-------SYSTEM MESSAGE--------
{system_message}
----------PROMPT---------
{prompt}
----------RESPONSE---------
{response}
"""
    return debug_string
