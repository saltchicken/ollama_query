import requests

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
    print(f"Data: {data}")
    response = requests.post(url, headers=headers, json=data)
    response = response.json()

    debug_string = pretty_print_prompt(prompt, system_message, response)
    return response.get("response", None), debug_string

def pretty_print_prompt(prompt, system_message, response):
    if system_message:
        estimated_tokens =  estimate_token_length(system_message) + estimate_token_length(prompt)
    else:
        estimated_tokens = estimate_token_length(prompt)
    debug_string = f"""
    Estimated tokens: {estimated_tokens}
    -------SYSTEM MESSAGE--------
     {system_message}
    ----------PROMPT---------
     {prompt}
    ----------RESPONSE---------
     {response}
    """
    return debug_string

def estimate_token_length(text: str) -> int:
    """Estimate the number of tokens in a string."""
    avg_chars_per_token = 4
    return max(1, len(text) // avg_chars_per_token)
