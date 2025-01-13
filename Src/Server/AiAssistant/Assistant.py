import json
import ollama
import os
from typing import Callable
from datetime import datetime
from langchain_ollama import ChatOllama
from ollama import ChatResponse
from Src.Server.AiAssistant.Functions.Holidays.Holiday import Holiday
from Src.Server.AiAssistant.Functions.Holidays.HolidayService import HolidayService

class Assistant:
    def __init__(self, use_online_sources: bool = False):
        self.__use_online_sources = use_online_sources
        self.__holiday_service = HolidayService(from_online_source=use_online_sources)
        self.__model = self.__config_model()


    def get_ai_output(self, prompt: str) -> str:
        time_context = f"[Data e hora atual: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] "
        return self.__run_llm(self.__model, time_context + prompt)



    @staticmethod
    def __get_tools() -> str:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'tools.json')
        file_content: str
        with open(file_path, 'r') as file:
            file_content = file.read()

        tools = json.loads(file_content)["tools"]
        return tools


    @staticmethod
    def __get_response_from_model(question: str) -> ChatResponse:
        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": question,
                    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                },
            ],
        )

        return response


    def __config_model(self) -> ChatOllama:
        model: ChatOllama = ChatOllama(model="llama3.2", format="json")
        tools = self.__get_tools()
        model = model.bind_tools(tools)  # type: ignore
        return model


    def __run_llm(self, llm_model, prompt_input) -> str:
        functions: dict[str, Callable[[str, int], list[Holiday]] | Callable[[str], ChatResponse]] = {
            "get_holidays": self.__holiday_service.get_holidays,
            "generic_response": self.__get_response_from_model
        }

        try:
            generic_error_message = "Não foi possível encontrar uma resposta para a pergunta"
            result = llm_model.invoke(prompt_input)
            if not result:
                raise ValueError("Resultado não encontrado")

            tool_calls = result.tool_calls
            if not tool_calls:
                raise ValueError("Chamadas de função não encontradas")

            # Function calls
            # Referencia: https://github.com/msamylea/Llama3_Function_Calling
            for tool_call in tool_calls:
                function_name: str = tool_call.get('name')
                function_parameters: dict[str, str] = tool_call.get('args')

                if not function_parameters or not function_name:
                    raise ValueError("Argumentos ou nome da função não encontrados")

                function = (functions.get(function_name))
                chat_response: ChatResponse

                # Feriados
                if function_name == "get_holidays":
                    state: str | None = function_parameters.get('state')
                    year_as_str: str | None = function_parameters.get('year')
                    year: int | None = int(year_as_str) if year_as_str else None
                    if state and year:
                        holidays_list: list[Holiday] = function(state=state, year=year)  # type: ignore

                        if holidays_list.__len__() == 0:
                            return "Nenhum feriado foi encontrado"

                        re_input = ("Dada essa pergunta: '" + prompt_input + "', os feriados são: "
                                    + str(holidays_list)
                                    + ". Responda a pergunta de forma resumida e direta e como se estivesse conversando oralmente."
                                    )

                        chat_response = self.__get_response_from_model(re_input)
                        if isinstance(chat_response.message.content, str):
                            return chat_response.message.content
                        else:
                            return generic_error_message

                    else:
                        print(f"Argumentos incompletos: {function_parameters}")


                # Resposta genérica
                elif function_name == "generic_response":
                    chat_response = function(question=prompt_input)  # type: ignore
                    if isinstance(chat_response.message.content, str):
                        return chat_response.message.content
                    else:
                        return generic_error_message


            raise Exception("Nenhuma função foi chamada")

        except Exception as e:
            print(f"Erro ao tentar responder: {e}")
            return "Desculpe, parece que houve um erro ao tentar responder. O que acha de reformular a pergunta?"
