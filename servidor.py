"""
servidor.py
------------
Essa é a "ponte" entre o robô físico (ESP32) e a IA.

Fluxo:
1. O ESP32 manda uma requisição HTTP com o texto que o estudante falou.
2. Esse servidor chama a IA (cliente_ia_gemini.py) e pega a resposta.
3. O servidor devolve a resposta em texto para o ESP32,
   que depois manda para a síntese de voz (parte da Maria).

O João é responsável por rodar e manter esse servidor.
"""

from flask import Flask, request, jsonify
from cliente_ia_gemini import gerar_resposta
from banco import obter_historico, salvar_mensagem
import uuid

app = Flask(__name__)


@app.route("/conversar", methods=["POST"])
def conversar():
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "erro": "Envie um JSON válido."
        }), 400

    personagem_id = dados.get("personagem")
    id_sessao = dados.get("sessao")
    pergunta = dados.get("mensagem")

    if not personagem_id or not pergunta or not id_sessao:
        return jsonify({
            "erro": "Envie 'personagem', 'sessao' e 'mensagem' no corpo da requisição."
        }), 400

    try:
        # Recupera o histórico da sessão no PostgreSQL
        historico = obter_historico(id_sessao)

        # Gera a resposta utilizando o histórico anterior
        resposta = gerar_resposta(
            personagem_id,
            historico,
            pergunta
        )

        # Salva a pergunta e a resposta no PostgreSQL
        salvar_mensagem(id_sessao, "user", pergunta)
        salvar_mensagem(id_sessao, "assistant", resposta)

        return jsonify({
            "resposta": resposta,
            "sessao": id_sessao
        })

    except Exception:
        app.logger.exception("Erro ao processar conversa.")

        return jsonify({
            "erro": "Não foi possível processar a conversa."
        }), 500


@app.route("/nova_conversa", methods=["POST"])
def nova_conversa():
    """Gera um identificador único para uma nova simulação."""

    id_sessao = str(uuid.uuid4())

    return jsonify({
        "status": "nova conversa iniciada",
        "sessao": id_sessao
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)