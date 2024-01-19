from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-3.5-turbo"

def load(name_archive):
    try:
        with open(name_archive, "r") as archive:
            data = archive.read()
            return data
    except IOError as err:
        print(f"Erro no carregamento de arquivo: {err}")

def save(name_archive, content):
    try:
        with open(name_archive, "w", encoding="utf-8") as archive:
            archive.write(content)
    except IOError as err:
        print(f"Erro ao salvar arquivo: {err}")

def transaction_analizer(list_transaction):
    print("1.Executando a análise de transação")

    prompt_system = """
    Analise as transações financeiras a seguir e identifique se cada uma delas é uma "Possível Fraude" ou deve ser "Aprovada". 
    Adicione um atributo "Status" com um dos valores: "Possível Fraude" ou "Aprovado".

    Cada nova transação deve ser inserida dentro da lista do JSON. 

    # Possíveis indicações de fraude
    - Transações com valores muito discrepantes
    - Transações que ocorrem em locais muito distantes um do outro

    Adote o formato de resposta abaixo para compor sua resposta.
    
    # Formato Saída 
    {
        "transacoes": [
            {
            "id": "id",
            "tipo": "crédito ou débito",
            "estabelecimento": "nome do estabelecimento",
            "horário": "horário da transação",
            "valor": "R$XX,XX",
            "nome_produto": "nome do produto",
            "localização": "cidade - estado (País)"
            "status": ""
            },
        ]
    } 
    """

    list_messages = [
        {
            "role": "system",
            "content": prompt_system
        },
        {
            "role": "user",
            "content": f"Considere o CSV abaixo, onde cada linha é uma transação diferente: {list_transaction}. Sua resposta deve adotar o #Formato de Resposta (apenas um json sem outros comentários)"
        }
    ]

    response = client.chat.completions.create(
        messages = list_messages,
        model=model,
        temperature=0
    )

    content = response.choices[0].message.content.replace("'", '"')
    print("\Conteúdo:", content)
    json_result = json.loads(content)
    print("\nJSON:", json_result)
    return json_result

def generate_opinion(transaction):
    print("2. Gerando um parecer para cada transação")

    prompt_system = f"""
    Para a seguinte transação, forneça um parecer, apenas se o status dela for de "Possível Fraude". Indique no parecer uma justificativa para que você identifique uma fraude.
    Transação: {transaction}

    ## Formato de Resposta
    "id": "id",
    "tipo": "crédito ou débito",
    "estabelecimento": "nome do estabelecimento",
    "horario": "horário da transação",
    "valor": "R$XX,XX",
    "nome_produto": "nome do produto",
    "localizacao": "cidade - estado (País)"
    "status": "",
    "parecer" : "Colocar Não Aplicável se o status for Aprovado"
    """

    list_messages = [
        {
            "role": "user",
            "content": prompt_system
        }
    ]

    response = client.chat.completions.create(
        messages = list_messages,
        model=model,
    )

    content = response.choices[0].message.content
    print("Finalizou a geração de parecer")
    return content

def generate_recommendation(opinion):
    print("3. Gerando recomendações")

    prompt_system = f"""
    Para a seguinte transação, forneça uma recomendação apropriada baseada no status e nos detalhes da transação da Transação: {opinion}

    As recomendações podem ser "Notificar Client", "Acionar setor Anti-Fraude" ou "Realizar Verificação Manual".
    Elas devem ser escrito no formato técnico.

    Inclua também uma classificação do tipo de fraude, se aplicável. 
    """

    list_messages = [
        {
            "role": "system",
            "content": prompt_system
        }
    ]

    response = client.chat.completions.create(
        messages = list_messages,
        model=model,
    )

    content = response.choices[0].message.content
    print("Finalizou a geração de recomendação")
    return content

list_transaction = load("./data/transacoes.csv")
transaction_analyzed = transaction_analizer(list_transaction)

for transaction in transaction_analyzed["transacoes"]:
    if transaction["status"] == "Possível Fraude":
        opinion = generate_opinion(transaction)
        print(opinion)
        recommendation = generate_recommendation(opinion)
        id_transaction = transaction["id"]
        product_transaction = transaction["nome_produto"]
        status_transaction = transaction["status"]
        save(f"./data/transaction-{id_transaction}-{product_transaction}-{status_transaction}.txt", recommendation)
