import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def conectar():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def salvar_mensagem(sessao_id, role, content):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO mensagens (sessao_id, role, content)
                VALUES (%s, %s, %s)
                """,
                (sessao_id, role, content)
            )



def obter_historico(sessao_id):
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT role, content
                FROM mensagens
                WHERE sessao_id = %s
                ORDER BY created_at ASC, id ASC
                """,
                (sessao_id,)
            )

            mensagens = cursor.fetchall()

            return [
                {"role": role, "content": content}
                for role, content in mensagens
            ]