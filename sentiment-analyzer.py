from openai import OpenAI
from dotenv import load_dotenv
import os
import openai

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-3.5-turbo"

def load(name_archive):
    try:
        with open(name_archive, "r") as archive:
            data = archive.read()
            return data
    except IOError as err:
        print(f"Erro: {err}")

def save(name_archive, content):
    try:
        with open(name_archive, "w", encoding="utf-8") as archive:
            archive.write(content)
    except IOError as err:
        print(f"Erro ao salvar arquivo: {err}")

def sentiment_analyzer(product):
    prompt_system = f"""
        Você é um analisador de sentimentos de avaliações de produtos.
        Escreva um parágrafo com até 50 palavras resumindo as avaliações e 
        depois atribua qual o sentimento geral para o produto.
        Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

        # Formato de Saída

        Nome do Produto:
        Resumo das Avaliações:
        Sentimento Geral: [utilize aqui apenas Positivo, Negativo ou Neutro]
        Ponto fortes: lista com três bullets
        Pontos fracos: lista com três bullets
    """
     
    prompt_user = load(f"./data/avaliacoes-{product}.txt")
    print(f"Iniciou a análise de sentimentos do produto {product}")

    list_messages = [
        {
            "role": "system",
            "content": prompt_system
        },
        {
            "role": "user",
            "content": prompt_user
        }
    ]

    try:
        response = client.chat.completions.create(
            messages = list_messages,
            model=model
        )

        text_response = response.choices[0].message.content
        save(f"./data/analise-{product}.txt", text_response)
    except openai.AuthenticationError as err:
        print(f"Erro de Autenticação: {err}")
    except openai.APIError as err:
        print(f"Erro de API: {err}")

list_products = ["Camisetas de algodão orgânico", "Jeans feitos com materiais reciclados", "Maquiagem mineral"]
for product in list_products:
    sentiment_analyzer(product)
