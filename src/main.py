import chat, setup, utils, os

# just to make sure for edge cases
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

setup.run()

if not chat.is_running():
    chat.init()

while True:
    response = ""

    prompt = input(f"({chat.model}) >>> ")

    if prompt.lower().strip() == "quit":
        utils.Exit()

    for chunk in chat.get_responce(prompt, chat.model):
        part = chunk['message']['content']
        print(part, end='', flush=True)
        response += part

    chat.update_history(response)

    print("\n\n")
