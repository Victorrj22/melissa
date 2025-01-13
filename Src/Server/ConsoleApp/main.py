from Src.Server.AiAssistant.Assistant import Assistant

assistant = Assistant(use_online_sources= True)

print("Faça uma pergunta à Melissa:")

while True:
    question = input("VOCÊ: ")
    if question == "sair":
        break

    response = assistant.get_ai_output(question)
    print("MELISSA:", response)