import requests

def ollama_query(model, prompt, system_message=None, verbose=False, host="localhost", port=11434):
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

    if verbose: pretty_print_prompt(prompt, system_message, response)
    return response.get("response", None)

def pretty_print_prompt(prompt, system_message, response):
    print("-------SYSTEM MESSAGE--------")
    print(system_message)
    print("----------PROMPT---------")
    print(prompt)
    print("----------RESPONSE---------")
    print(response)
    print("\n\n")
    if system_message:
        print(f"Estimated tokens: {estimate_token_length(system_message) + estimate_token_length(prompt)}")
    else:
        print(f"Estimated tokens: {estimate_token_length(prompt)}")

def estimate_token_length(text: str) -> int:
    """Estimate the number of tokens in a string."""
    avg_chars_per_token = 4
    return max(1, len(text) // avg_chars_per_token)
