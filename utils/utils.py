import requests
import json
import os

def query_ollama(prompt, model, temperature=0.7, system_prompt=""):
    
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "temperature": temperature,
        "system": system_prompt
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        return response.json().get("response", "Error: No response from Ollama.")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    
def list_models():
    model_path = f'{os.path.expanduser("~")}/.ollama/models/manifests/registry.ollama.ai/library/'
    if not os.path.exists(model_path):
        return []

    models = []
    for model in os.listdir(model_path):
        model_dir = os.path.join(model_path, model)
        if os.path.isdir(model_dir):
            subdirs = os.listdir(model_dir)
            models.extend([f"{model}:{subdir}" for subdir in subdirs])
        else:
            models.append(model)
    return models