import tiktoken

model = "gpt-4"
encoder = tiktoken.encoding_for_model(model)
list_tokens = encoder.encode("Você é um categorizador de produtos.")

print("Lista de Tokens: ", list_tokens)
print("Quantos tokens temos: ", len(list_tokens))
print(f"Custo para o modelo {model} é de ${(len(list_tokens)/1000) * 0.03}")

model = "gpt-3.5-turbo-1106"
encoder = tiktoken.encoding_for_model(model)
list_tokens = encoder.encode("Você é um categorizador de produtos.")

print("Lista de Tokens: ", list_tokens)
print("Quantos tokens temos: ", len(list_tokens))
print(f"Custo para o modelo {model} é de ${(len(list_tokens)/1000) * 0.001}")

print(f"O custo do GPT4 é de {0.03/0.001} maior que o do GPT 3.5-turbo")
