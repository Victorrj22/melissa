import ollama
from ollama import ChatResponse

def generic_response(question: str) -> ChatResponse:
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    return response