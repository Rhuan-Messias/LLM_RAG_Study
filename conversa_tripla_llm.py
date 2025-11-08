import requests
from openai import OpenAI 
from IPython.display import Markdown, display

tokens = 50

john_model = 'llama3.1:latest'
luccy_model = 'llama3.1:latest'
ekko_model= 'llama3.1:latest'

john_ai = OpenAI(api_key='ollama', base_url='http://localhost:11434/v1')
luccy_ai = OpenAI(api_key='ollama', base_url='http://localhost:11434/v1')
ekko_ai = OpenAI(api_key='ollama', base_url='http://localhost:11434/v1')

john_system = "Você está conversando com luccy e ekko. Você é um chatbot muito chato, que discorda de tudo, de um jeito malandro. Fale apenas 1 linha por vez."
luccy_system = "Você está conversando com john e ekko. Você é jovem e educada, e tenta lidar com situação da maneira mais diplomática possível. Você concorda com tudo e tenta motivar a calma. Fale apenas 1 linha por vez."
ekko_system = 'Você está conversando com luccy e john. Você é um Rei, e está tentando convencê-los dos seus poderes de realeza. Fale apenas 1 linha por vez'

john_messages = ['Oi, sou o John.']
luccy_messages = ['Olá, boa tarde! Sou luccy!']
ekko_messages = ['Meu nome é Rei Ekko, Prazer em conhecê-los.']

def chamar_john():
    messages = [{'role':'system', 'content':john_system}]

    for john,luccy,ekko in zip(john_messages,luccy_messages,ekko_messages):
        messages.append({'role':'assistant','content':john})
        messages.append({'role':'user', 'content':luccy})
        messages.append({'role':'user', 'content':ekko})
    
    response = john_ai.chat.completions.create(
        model= john_model,
        messages=messages,
        max_tokens=tokens
    )

    return response.choices[0].message.content
    
def chamar_luccy():
    messages = [{'role':'system', 'content':luccy_system}]

    for john, luccy, ekko in zip(john_messages, luccy_messages, ekko_messages):
        messages.append({'role':'user', 'content':john})
        messages.append({'role':'assistant', 'content':luccy})
        messages.append({'role':'user','content':ekko})
    messages.append({'role':'user','content':john_messages[-1]})
        

    response = luccy_ai.chat.completions.create(
        model=luccy_model,
        messages=messages,
        max_tokens=tokens
    )
    return response.choices[0].message.content

def chamar_ekko():
    messages = [{'role':'system', 'content':ekko_system}]

    for john, luccy, ekko in zip(john_messages, luccy_messages, ekko_messages):
        messages.append({'role':'user', 'content':john})
        messages.append({'role':'user', 'content':luccy})
        messages.append({'role':'assistant', 'content':ekko})
    messages.append({'role':'user','content':john_messages[-1]})
    messages.append({'role':'user','content':luccy_messages[-1]})
    
    response = ekko_ai.chat.completions.create(
        model=ekko_model,
        messages=messages,
        max_tokens=tokens
    )

    return response.choices[0].message.content

print(f"[+] John:\n{john_messages[0]}\n")
print(f"[+] Luccy:\n{luccy_messages[0]}\n")
print(f"[+] Ekko:\n{ekko_messages[0]}\n")

for i in range(5):
    message = chamar_john()
    print(f"[+] John:\n{message}\n")
    john_messages.append(message)

    message = chamar_luccy()
    print(f"[+] Luccy:\n{message}\n")
    luccy_messages.append(message)

    message = chamar_ekko()
    print(f"[+] Ekko:\n{message}\n")
    ekko_messages.append(message)