from tkinter import messagebox
import subprocess

def Exit() -> None:
    from chat import ollama_process
    
    ollama_process.terminate()
    ollama_process.wait()

    quit(0)

def show_error(message):
    messagebox.showerror("Error", message)