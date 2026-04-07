from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Zawa 2.0 está viva 🧠"

if __name__ == "__main__":
    app.run()
