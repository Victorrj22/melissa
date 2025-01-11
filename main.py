from typing import Callable
from langchain_ollama import ChatOllama
import Holidays as Holidays
from Holidays import Holiday
import Generic as Generic
from ollama import ChatResponse

question = "[data atual: 10/01/2025] Quais feriados nesse mes em Sao Paulo?"
model = ChatOllama(model="llama3.2", format="json")

# Aqui é feito o 'treinamento' da IA de acordo com cada função
model = model.bind_tools(  # type: ignore
    tools=[
        {
            "name": "get_holidays",
            "description": "Get the holidays of the year for a specific state",
            "parameters": {
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "The state abbreviation to get holidays for ('SP', 'RJ', 'ES')."
                    },
                    "year": {
                        "type": "integer",
                        "description": "The year to get holidays for"
                    }
                },
                "required": ["state", "year"]
            }
        },
        {

            "name": "generic_response",
            "description": "Get a generic response for generic questions",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "A generic question about anything"
                    }
                },
                "required": ["question"]
            }
        }
    ],
)

functions: dict[str, Callable[[str, int, str], list[Holiday]] | Callable[[str], ChatResponse]] = {
    "get_holidays": Holidays.get_holidays,
    "generic_response": Generic.generic_response
}

def invoke_and_run(llm_model, prompt) -> str:
    try:
        generic_error_message = "Não foi possível encontrar uma resposta para a pergunta"
        result = llm_model.invoke(prompt)
        if not result:
            return generic_error_message

        tool_calls = result.tool_calls
        if not tool_calls:
            return generic_error_message

        # Dentro de tool_calls ficam os mapeamentos que a IA realizou conforme o input e o método reconhecido
        for tool_call in tool_calls:
            function_name: str = tool_call.get('name')
            function_parameters: dict[str, str] = tool_call.get('args')

            if not function_parameters or not function_name:
                return f"Função ou argumentos ausentes em: {tool_call}"

            function: Callable[[str, int, str], list[Holiday]] | Callable[[str], ChatResponse] | None = (
                functions.get(function_name))
            chat_response: ChatResponse

            if function is Holidays.get_holidays:
                state: str | None = function_parameters.get('state')
                year_as_str: str | None = function_parameters.get('year')
                year: int | None = int(year_as_str) if year_as_str else None
                if state and year:
                    holidays_list: list[Holiday] = function(state=state, year=year, token=Holidays.token)  # type: ignore

                    re_input = ("Dada essa pergunta: '" + question + "', os feriados são: "
                                + str(holidays_list)
                                + ". Responda a pergunta de forma resumida e direta e como se estivesse conversando oralmente."
                                )

                    chat_response = Generic.generic_response(re_input)
                    if isinstance(chat_response.message.content, str):
                        return chat_response.message.content
                    else:
                        return generic_error_message

                else:
                    print(f"Argumentos incompletos: {function_parameters}")

            # Caso o modelo identifique que é uma pergunta genérica, entra no fluxo do modelo Ollama
            elif function is Generic.generic_response:
                assert function is Generic.generic_response
                chat_response = function(question=question)  # type: ignore
                if isinstance(chat_response.message.content, str):
                    return chat_response.message.content
                else:
                    return generic_error_message

        return generic_error_message

    except Exception as e:
        return f"Erro ao executar a função: {e}"


print(invoke_and_run(model, question))
