from ollama import Client

ollama_client = Client()

def ask_ollama(prompt: str, model_name: str = "llama3.1:8b"):
    response = ollama_client.chat(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Check the type and keys
    if isinstance(response, dict) and "content" in response:
        return response["content"]
    elif isinstance(response, list) and len(response) > 0 and "content" in response[0]:
        return response[0]["content"]
    else:
        # fallback: return full response as string for debugging
        return str(response)
