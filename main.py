from langchain_ollama import ChatOllama
import Holidays as holidays
import Generic as generic
from ollama import ChatResponse

# question = "Estamos no mês de Janeiro de 2025, quais são os feriados desse nês em SP?";
question = "[data atual: 10/01/2025] Quais feriados nesse mes em Sao Paulo?"
model=ChatOllama(model="llama3.2", format="json")

#Aqui é feito o 'treinamento' da IA de acordo com cada função
model = model.bind_tools(
    tools = [
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
                    "year":{
                        "type": "integer",
                        "description": "The year to get holidays for"
                    }
                },
                "required": ["state","year"]
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

functions = {
    "get_holidays": holidays.get_holidays,
    "generic_response": generic.generic_response
}

def invoke_and_run(model, invoke_arg):
    result = model.invoke(invoke_arg)
    if result:
        tool_calls = result.tool_calls
        #Dentro de tool_calls ficam os mapeamentos que a IA realizou de acordo com o input e o metodo reconhecido
        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.get('name')
                #Esses são os parâmetros para a função reconhecida
                arguments = tool_call.get('args')
                if arguments and function_name:
                    function = functions.get(function_name)
                    #Por enquanto temos apenas 1 verificação para get_holidays. Quando houver outras funções, colocaremos em outros 'else'
                    if function and function_name == 'get_holidays':
                        state = arguments.get('state')
                        year = arguments.get('year')
                        if state and year:
                            #Chama a função passando os parâmetros reconhecidos
                            holidays_list = function(state=state, year=year, token=holidays.token)
                            re_input = "Dada essa pergunta: '" + question + "', os feriados são: " + str(holidays_list) + ". Responda a pergunta de forma resumida e direta e como se estivesse conversando oralmente."
                            response: ChatResponse = generic.generic_response(re_input)
                            print(response.message.content)
                        else:
                            print(f"Argumentos incompletos: {arguments}")
                    #Caso o modelo identifique que é uma pergunta genérica, entra no fluxo do modelo Ollama
                    elif function and function_name == 'generic_response':
                        response = generic.generic_response(question=question)
                        message = response.get('message')
                        content = message.get('content')
                        print('Pergunta:' + question)
                        print ('Resposta:' + content)
                else:
                    print(f"Função ou argumentos ausentes em: {tool_call}")

invoke_and_run(model, question)