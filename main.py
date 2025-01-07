from langchain_ollama import ChatOllama
import Holidays as holidays

question = "Me fala quais foram os feriados do ano passado no RJ";

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
    ],
)

functions = {
    "get_holidays": holidays.get_holidays
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
                            print("Question: " + question)
                            for holiday in holidays_list:
                                print(holiday)
                        else:
                            print(f"Argumentos incompletos: {arguments}")
                else:
                    print(f"Função ou argumentos ausentes em: {tool_call}")

invoke_and_run(model, question)