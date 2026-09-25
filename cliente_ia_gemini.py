"""
cliente_ia_gemini.py
----------------------
Versão alternativa do cliente_ia.py, usando a API do Google Gemini


Para usar essa versão no lugar da API da Anthropic, no servidor.py troque:
    from cliente_ia import gerar_resposta
por:
    from cliente_ia_gemini import gerar_resposta
"""

import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Carrega a chave de API guardada no arquivo .env
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Carrega os personagens (Ana e Pedro) do mesmo arquivo usado pela versão Anthropic
with open("personagens.json", "r", encoding="utf-8") as f:
    PERSONAGENS = json.load(f)


def gerar_resposta(personagem_id: str, historico: list, pergunta_estudante: str) -> str:
    """
    personagem_id: "ana" ou "pedro"
    historico: lista de mensagens já trocadas, no formato [{"role": "user"/"assistant", "content": "..."}]
    pergunta_estudante: texto que o estudante acabou de falar/digitar
    """

    if personagem_id not in PERSONAGENS:
        raise ValueError(f"Personagem '{personagem_id}' não encontrado.")

    prompt_sistema = PERSONAGENS[personagem_id]["prompt_sistema"]

    # O Gemini usa "role: model" no lugar de "role: assistant" -> precisa converter
    contents = []
    for msg in historico:
        papel = "model" if msg["role"] == "assistant" else "user"
        contents.append(types.Content(role=papel, parts=[types.Part(text=msg["content"])]))

    contents.append(types.Content(role="user", parts=[types.Part(text=pergunta_estudante)]))

    resposta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=prompt_sistema,
            max_output_tokens=300,
        ),
    )

    return resposta.text


# Teste rápido: rode "python cliente_ia_gemini.py" para testar sozinho, sem o servidor
if __name__ == "__main__":
    historico_teste = []
    resposta = gerar_resposta("pedro", historico_teste, "Oi, como você está se sentindo hoje?")
    print("Pedro respondeu:", resposta)
