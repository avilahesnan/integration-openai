from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-3.5-turbo"


def categorizes_product(name_product, list_product_possible):
    prompt_system = f"""
        Você é um categorizador de produtos.
        Você deve assumir as categorias presentes na lista abaixo.

        # Lista de Categorias Válidas
        {list_product_possible.split(",")}

        # Formato da Saída
        Produto: Nome do Produto
        Categoria: apresente a categoria do produto

        # Exemplo de Saída
        Produto: Escova elétrica com recarga solar
        Categoria: Eletrônicos Verdes
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": prompt_system
            },
            {
                "role": "user",
                "content": name_product
            }
        ],
        temperature=1,
        max_tokens=200
    )
    return response.choices[0].message.content

categories_valid = input("Informe as categorias válidas, separando por vírgula: ")

while True:
    name_product = input("Digite o nome de um produto: ")
    text_response = categorizes_product(name_product, categories_valid)
    print(text_response)
