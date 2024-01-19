from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response =client.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages= [
        {
            'role': 'system',
            'content': 'Gere nomes masculinos para um filme de zumbis'
        },
        {
            'role': 'user',
            'content': 'Gere 5 nomes'
        }
    ]
)
print(response.choices[0].message.content)
