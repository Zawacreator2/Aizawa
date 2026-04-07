from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_URL = "https://models.inference.ai.azure.com/chat/completions"
API_KEY = os.getenv("GITHUB_KEY")

CEREBRO_PROMPT = """
Você é o cérebro da Zawa.

Responda apenas com JSON:

{
  "complexidade": "simples | medio | complexo | stack",
  "apis": ["clima", "noticias", "stack", "wolfram"]
}
"""

@app.route("/")
def home():
    return "Zawa 2.0 está viva 🧠"

@app.route("/cerebro", methods=["POST"])
def cerebro():
    mensagem = request.json.get("mensagem", "")

    if not mensagem:
        return jsonify({"erro": "mensagem vazia"})

    try:
        resposta = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": CEREBRO_PROMPT},
                    {"role": "user", "content": mensagem}
                ],
                "temperature": 0,
                "max_tokens": 100
            }
        )

        data = resposta.json()
        content = data["choices"][0]["message"]["content"]

        import json
        try:
            parsed = json.loads(content)
        except:
            parsed = {
                "complexidade": "medio",
                "apis": []
            }

        return jsonify(parsed)

    except Exception as e:
        return jsonify({
            "complexidade": "medio",
            "apis": [],
            "erro": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
