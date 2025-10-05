from ollama import Client

ollama_client = Client()

def ask_ollama(prompt: str, model_name: str = "deepseek-r1:8b"):
    response = ollama_client.chat(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    return response['content']
