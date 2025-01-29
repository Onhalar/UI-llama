import chat
import setup
import utils

chat.init()

print("select a model: ", chat.get_available_models())

while True:
    try:
        chat.select_model(input(">>> "))
        break
    except ValueError:
        pass

print("\n\n")

while True:
    response = ""

    prompt = input(">>> ")

    if prompt.lower().strip() == "quit":
        utils.Exit()

    for chunk in chat.get_responce(prompt, chat.model):
        part = chunk['message']['content']
        print(part, end='', flush=True)
        response += part

    chat.update_history(response)

    print("\n\n")
