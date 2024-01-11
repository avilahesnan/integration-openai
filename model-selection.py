from openai import OpenAI
from dotenv import load_dotenv
import os
import tiktoken

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-3.5-turbo"

encoder = tiktoken.encoding_for_model(model)

def load(name_archive):
    try:
        with open(name_archive, "r") as archive:
            data = archive.read()
            return data
    except IOError as e:
        print(f"Erro: {e}")

prompt_system = """
Identifique o perfil de compra para cada cliente a seguir.

O formato de saída deve ser:

cliente - descreva o perfil do cliente em 3 palavras
"""

prompt_user = load("data\lista_de_compras_100_clientes.csv")

list_tokens = encoder.encode(prompt_system + prompt_user)
number_tokens = len(list_tokens)
print(f"Número de tokens na entrada: {number_tokens}")
expected_output_size = 2048

if number_tokens >= 4096 - expected_output_size:
    model = "gpt-3.5-turbo-1106"

print(f"Modelo escolhido: {model}")

lista_mensagens = [
        {
            "role": "system",
            "content": prompt_system
        },
        {
            "role": "user",
            "content": prompt_user
        }
    ]

resposta = client.chat.completions.create(
    messages = lista_mensagens,
    model=model
)

print(resposta.choices[0].message.content)
