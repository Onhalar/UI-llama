import chat, utils
from tkinter import Tk, PhotoImage, END
from tkinter.ttk import *
from threading import Thread

# just to make sure for edge cases
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

def _return(window: Tk, model: Combobox, labels_to_update: tuple[Label]) -> None: # '_' means an internal function and it should not be visible outside of this file
    chat.set_model(model.get())
    for label in labels_to_update:
        label.config(text=chat.model)
    utils.Exit(window)

def _import_model(options_menu: Combobox, model: Entry):
    entry = model.get().strip().lower()
    try:
        utils.show_message("This might take a while...\n\nYou will see a popup window upon import's compleation.")
        chat.import_model(entry)
        utils.show_message("Model successfully imported!")
        if entry not in options_menu["values"]:
            options_menu['values'] += tuple([entry])
        model.delete(0, END)
    except Exception as e:
        utils.show_error(e)

def _remove_model(model: Entry):
    entry = model.get().strip().lower()
    try:
        chat.remove_model(entry)
        models.remove(entry)
        utils.show_message("Model successfully deleted!")
        model.delete(0, END)
    except Exception as e:
        utils.show_error(e)

def force_exit_setup(window: Tk):
    if chat.model != "":
        utils.Exit(window)
    else:
        utils.show_error("No model selected, exitting app...")
        utils.Exit()

def run(*labels_to_update: Label) -> None:
    global models

    if not chat.is_running():
        chat.init()

    main = Tk()
    main.iconbitmap(PhotoImage('../res/setup.ico'))
    main.title('UI-llama setup')
    main.resizable(False, False)
    main.protocol('WM_DELETE_WINDOW', lambda window = main : force_exit_setup(window))

    container = Frame(main)

    Label(container, text="Please select a model", anchor="center").grid(column=0, row=0, columnspan=2)

    models = chat.get_available_models()

    model_selector = Combobox(container, state="readonly",  values= models)
    model_selector.grid(column=0, row=1)

    model_selector.set('[NO MODELS FOUND]' if len(models) == 0 else models[0])

    Button(container, text='Select', command= lambda window = main, model = model_selector: _return(window, model, labels_to_update) ).grid(column=1, row=1)

    Separator(container, orient='horizontal').grid(column=0, row=2, columnspan=2, pady= 15, sticky='EW')

    selected_model = Entry(container)
    selected_model.grid(column=0, row=3, columnspan=2, sticky='EW')

    Button(container, text='Import model', command= lambda : Thread(target= lambda : _import_model(model_selector, selected_model)).start()).grid(column=0, row=4, sticky='EW')
    Button(container, text='Remove model', command= lambda : _remove_model(selected_model)).grid(column=1, row=4, sticky='EW')

    container.pack(padx= 5, pady= 5)

    main.mainloop()

if __name__ == '__main__':
    run()