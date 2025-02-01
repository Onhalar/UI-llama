from tkinter import messagebox, Tk

def Exit(window: Tk = None) -> None:
    from chat import ollama_process
    
    ollama_process.terminate()
    ollama_process.wait()

    if window is None:
        quit(0)
    else:
        window.destroy()

def show_error(message):
    messagebox.showerror("Error", message)

def show_message(message):
    messagebox.showinfo("info", message)