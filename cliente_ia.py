"""
cliente_ia.py
--------------
Responsável por: carregar o personagem escolhido e enviar a conversa
para a API de IA, devolvendo a resposta em texto.

Esse é o "coração" do trabalho do João dentro da Equipe de IA.
"""

import os
import json
from dotenv import load_dotenv
import anthropic

# Carrega a chave de API guardada no arquivo .env
load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Carrega os personagens (Ana e Pedro) do arquivo criado pela Sara e pelo Richard
with open("personagens.json", "r", encoding="utf-8") as f:
    PERSONAGENS = json.load(f)


def gerar_resposta(personagem_id: str, historico: list, pergunta_estudante: str) -> str:
    """
    personagem_id: "ana" ou "pedro"
    historico: lista de mensagens já trocadas na conversa (mantida pelo Diego)
    pergunta_estudante: texto que o estudante acabou de falar/digitar
    """

    if personagem_id not in PERSONAGENS:
        raise ValueError(f"Personagem '{personagem_id}' não encontrado.")

    prompt_sistema = PERSONAGENS[personagem_id]["prompt_sistema"]

    # Monta o histórico da conversa no formato que a API espera
    mensagens = historico + [{"role": "user", "content": pergunta_estudante}]

    resposta = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=prompt_sistema,
        messages=mensagens,
    )

    texto_resposta = resposta.content[0].text
    return texto_resposta


# Teste rápido: rode "python cliente_ia.py" para testar sozinho, sem o servidor
if __name__ == "__main__":
    historico_teste = []
    resposta = gerar_resposta("pedro", historico_teste, "Oi, como você está se sentindo hoje?")
    print("Pedro respondeu:", resposta)
