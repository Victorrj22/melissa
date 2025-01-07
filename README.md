ANTES DE QUALQUER COISA:
-

Monte uma imagem Docker do Ollama:
- docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

No terminal do Doccker, com o Ollama rodando, rode o seguinte comando:
- ollama pull llama3.2

O que foi necessário instalar?
-

- pip install ollama
- pip install langchain_ollama

APIs
-
- Feriados: https://api.invertexto.com/api-feriados (3k req/mês)
