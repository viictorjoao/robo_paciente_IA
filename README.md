# Passo a passo do João — Integração da IA

## Ferramentas necessárias

- **Python 3.10+** instalado no computador
- **Editor de código:** VS Code
- **Conta na API de IA** (neste guia, a API da Anthropic — Claude). Dá para trocar por outra API de IA generativa, o código muda pouco.
- **Postman** ou o comando `curl` (para testar o servidor antes do ESP32 estar pronto)
- **Git/GitHub** (opcional, mas recomendado para versionar o código com a equipe)

## Passo 1 — Preparar o ambiente

```bash
# Criar uma pasta para o projeto e entrar nela
mkdir robo_paciente_ia
cd robo_paciente_ia

# Criar um ambiente virtual (isola as bibliotecas do projeto)
python -m venv venv

# Ativar o ambiente virtual
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar as bibliotecas necessárias
pip install -r requirements.txt
```

## Passo 2 — Configurar a chave da API

1. Copie o arquivo `.env.example` e renomeie para `.env`.
2. Crie uma conta em https://console.anthropic.com (ou na API escolhida pela equipe).
3. Gere uma chave de API e cole dentro do `.env`:

```
ANTHROPIC_API_KEY=sua_chave_aqui
```

## Passo 3 — Testar a conexão com a IA (sem servidor ainda)

Rode o arquivo `cliente_ia.py` sozinho para garantir que a IA responde corretamente:

```bash
python cliente_ia.py
```

Se aparecer a resposta do Pedro no terminal, a conexão com a API está funcionando.

## Passo 4 — Subir o servidor (a "ponte" com o ESP32)

```bash
python servidor.py
```

O servidor vai rodar em `http://localhost:5000` (ou no IP da máquina, na rede Wi-Fi).

## Passo 5 — Testar o servidor com o Postman ou curl

```bash
curl -X POST http://localhost:5000/conversar \
  -H "Content-Type: application/json" \
  -d '{"personagem": "ana", "sessao": "teste1", "mensagem": "Oi, tudo bem?"}'
```

Resposta esperada:

```json
{"resposta": "Oi! Tudo ótimo, e com você? 😊"}
```

Para testar o Pedro, é só trocar `"personagem": "ana"` por `"personagem": "pedro"`.

## Passo 6 — Reiniciar uma conversa

Antes de cada nova simulação, chamar:

```bash
curl -X POST http://localhost:5000/nova_conversa \
  -H "Content-Type: application/json" \
  -d '{"sessao": "teste1"}'
```

## Passo 7 — Integrar com o ESP32 (Equipe 1)

Quando o hardware estiver pronto, o ESP32 vai:
1. Gravar o áudio do estudante (parte da Maria transforma isso em texto).
2. Mandar esse texto para `http://IP_DO_SERVIDOR:5000/conversar`.
3. Receber a resposta em texto e mandar para a síntese de voz.

O João precisa garantir que o computador rodando o `servidor.py` esteja na
**mesma rede Wi-Fi** do ESP32, e passar o IP correto para a Equipe 1.

## Alternativa gratuita: Google Gemini

Se não quiser usar cartão de crédito, dá para usar a API do Google Gemini, que
tem uma camada gratuita sem cobrança inicial.

1. Instale a biblioteca do Gemini no lugar da Anthropic:
   ```bash
   pip install -r requirements_gemini.txt
   ```
2. Vá em https://aistudio.google.com/app/apikey, faça login com uma conta
   Google e clique em "Create API key" — não pede cartão de crédito.
3. Cole a chave no `.env`:
   ```
   GEMINI_API_KEY=sua_chave_aqui
   ```
4. No arquivo `servidor.py`, troque a linha:
   ```python
   from cliente_ia import gerar_resposta
   ```
   por:
   ```python
   from cliente_ia_gemini import gerar_resposta
   ```
5. Teste do mesmo jeito do Passo 3, mas rodando:
   ```bash
   python cliente_ia_gemini.py
   ```

O resto do projeto (servidor, personagens, integração com o ESP32) continua
exatamente igual — só o "motor" da IA muda.

## Passo 8 — Ajustes finais antes da AV1

- Testar os dois personagens várias vezes seguidas, com perguntas diferentes.
- Confirmar que a IA nunca sai do personagem nem se autodiagnostica.
- Ajustar `max_tokens` em `cliente_ia.py` se as respostas estiverem muito longas ou curtas.
- Combinar com o Diego a melhor forma de guardar o histórico (por enquanto está em memória — se o servidor reiniciar, perde a conversa).
