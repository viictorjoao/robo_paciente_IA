from banco import salvar_mensagem, obter_historico
import uuid

sessao = str(uuid.uuid4())

salvar_mensagem(sessao, "user", "Olá, como você está?")
salvar_mensagem(sessao, "assistant", "Estou um pouco ansioso.")

historico = obter_historico(sessao)

print(historico)