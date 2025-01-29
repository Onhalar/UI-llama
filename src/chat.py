import ollama
import subprocess

import utils

history = []
model = ""

ollama_process: subprocess.Popen

def init() -> None:
    global ollama_process
    ollama_process = subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def terminate() -> None:
    if ollama_process.poll() is None:
        ollama_process.terminate()
        ollama_process.wait()

def get_available_models() -> list[str]:
    return [llm["model"] for llm in ollama.list().model_dump()["models"]]

def get_responce(prompt: str, current_model: str = model, chat: list = history.copy()) -> str | None:
    global history
    try:
        chat += [{'role': 'user', 'content': prompt}]
        stream = ollama.chat(current_model, messages=chat, stream=True)
        history = chat
        return stream
    except Exception as e:
        utils.show_error(e)

def update_history(content: str, role: str = 'assistant'):
    global history
    history.append({'role': role, 'content': content})

def import_model(model: str):
    ollama.pull(model)

def select_model(selected_model: str):
    models = get_available_models()

    if models == []:
        input("No models found, exitting...")
        utils.Exit()

    if selected_model not in models:
        raise ValueError(f"Model '{selected_model}' not found.")
    
    global model
    model = selected_model