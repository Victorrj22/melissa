from ..AiAssistant import Assistant  # type: ignore

assistant = Assistant.Assistant(model_name="llama3.1", use_online_sources=True)

print("Faça uma pergunta à Melissa:")

while True:
    question = input("VOCÊ: ")
    if question == "sair":
        break

    response = assistant.get_ai_output(question)
    print("MELISSA:", response)
