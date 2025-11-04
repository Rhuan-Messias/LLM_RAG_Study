import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import sys

'''
   dependencias
    requests
    bs4
    openai

    modo de uso: 
    python3 <arquivo.py> <url> 
'''

if len(sys.argv) == 1:
        print("Nenhum Argumento Usado.")
else:
    for i, arg in enumerate(sys.argv[1:], start=1):
        print(f"Argumento {i}: {arg}")
        url = arg

ollama_base_url = 'http://localhost:11434/v1'

def fetch_website_contents(url):
    """
    retorna títulos e conteúdos do website;
    limite de 2 mil caracteres de conteúdo
    """
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "Título não encontrado"
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return (title + text)[:2_000]

ollama = OpenAI(base_url=ollama_base_url,
                api_key='ollama')

mensagem = [{'role':'system', 'content':'Faça um breve resumo da página enviada'},
            {'role':'user', 'content':fetch_website_contents(url)}]

response = ollama.chat.completions.create(
    model='llama3.2',
    messages=mensagem
)

print(response.choices[0].message.content)
