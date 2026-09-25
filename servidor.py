"""
servidor.py
------------
Essa é a "ponte" entre o robô físico (ESP32, da Equipe 1) e a IA.

Fluxo:
1. O ESP32 manda uma requisição HTTP com o texto que o estudante falou.
2. Esse servidor chama a IA (cliente_ia.py) e pega a resposta.
3. O servidor devolve a resposta em texto para o ESP32,
   que depois manda para a síntese de voz (parte da Maria).

O João é responsável por rodar e manter esse servidor.
"""

from flask import Flask, request, jsonify
from cliente_ia import gerar_resposta

app = Flask(__name__)

# Guarda o histórico de cada conversa em andamento (simplificado, em memória)
# O Diego vai evoluir isso depois para algo mais robusto (ex: banco de dados)
conversas = {}


@app.route("/conversar", methods=["POST"])
def conversar():
    dados = request.get_json()

    personagem_id = dados.get("personagem")       # "ana" ou "pedro"
    id_sessao = dados.get("sessao", "padrao")      # identifica a conversa em andamento
    pergunta = dados.get("mensagem")

    if not personagem_id or not pergunta:
        return jsonify({"erro": "Envie 'personagem' e 'mensagem' no corpo da requisição."}), 400

    historico = conversas.get(id_sessao, [])

    try:
        resposta = gerar_resposta(personagem_id, historico, pergunta)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

    # Atualiza o histórico da conversa
    historico.append({"role": "user", "content": pergunta})
    historico.append({"role": "assistant", "content": resposta})
    conversas[id_sessao] = historico

    return jsonify({"resposta": resposta})


@app.route("/nova_conversa", methods=["POST"])
def nova_conversa():
    """Reinicia o histórico de uma sessão (usar antes de começar uma nova simulação)."""
    dados = request.get_json()
    id_sessao = dados.get("sessao", "padrao")
    conversas[id_sessao] = []
    return jsonify({"status": "conversa reiniciada"})


if __name__ == "__main__":
    # host="0.0.0.0" permite que o ESP32, na mesma rede Wi-Fi, acesse esse servidor
    app.run(host="0.0.0.0", port=5000, debug=True)
