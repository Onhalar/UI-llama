import chat, setup, utils, os
from tkinter import Tk, PhotoImage, Text, DISABLED, NORMAL, END
from tkinter.ttk import *
from time import sleep
from threading import Thread

# just to make sure for edge cases
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

setup.run()

if not chat.is_running():
    chat.init()

def update_text(output: Text, text: str, smooth = False, wait = 0.01):
    output.config(state=NORMAL)
    if smooth:
        for letter in text:
            output.insert(END, letter)
            output.see(END)
            sleep(0.01)
    else:
        output.insert(END, text)
        output.see(END)
    output.config(state=DISABLED)

def message(output: Text, user_input: Text):
    prompt = user_input.get("1.0", END)

    user_input.delete("1.0", END)

    update_text(output, f"Prompt: {prompt}\nOutput:\n", smooth= True)

    response = ""
    for chunk in chat.get_responce(prompt, chat.model):
        part = chunk['message']['content']
        update_text(output, part, smooth= True, wait=0.0075)
        response += part

    chat.update_history(response)
    update_text(output, "\n<END>\n\n", smooth= True)

def UI():
    main = Tk()
    main.iconbitmap(PhotoImage('../res/main.ico'))
    main.title('UI-llama')
    main.resizable(False, False)
    main.protocol('WM_DELETE_WINDOW', lambda : utils.Exit())

    container = Frame(main)

    output = Text(container, state=DISABLED, borderwidth=0)
    output.grid(column=0, row=0, columnspan=3, sticky='EW')

    separator = Frame(container)

    separator.columnconfigure(index=0, weight=1)

    Separator(separator, orient='horizontal').grid(column=0, row=0, sticky='EW')
    Label(separator, text=chat.model).grid(column=1, row=0)

    separator.grid(column=0, row=1, columnspan=3, sticky='EW')

    user_input = Text(container, height=2)
    user_input.grid(column=0, row=2, columnspan=2, rowspan=2, sticky='NS')

    Button(container, text='send', command= lambda : Thread(target= lambda output = output, user_input = user_input : message(output, user_input)).start()).grid(column=2, row=2, padx=5)
    Button(container, text='options', command=setup.run).grid(column=2, row=3, padx=5)

    container.pack(pady=5, padx=5)

    main.mainloop()


if __name__ == '__main__':
    UI()