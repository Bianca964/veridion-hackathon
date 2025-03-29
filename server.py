from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Simulăm un set de cuvinte
WORDS = ["rock", "paper", "scissors"]
current_round = 1
game_status = {"status": "ongoing"}

@app.route("/get-word", methods=["GET"])
def get_word():
    global current_round
    return jsonify({"word": random.choice(WORDS), "round": current_round})

@app.route("/status", methods=["GET"])
def status():
    return jsonify(game_status)

@app.route("/submit-word", methods=["POST"])
def submit_word():
    global current_round
    data = request.get_json()
    print(f"Received: {data}")
    current_round += 1  # Simulăm trecerea la următoarea rundă
    return jsonify({"message": "Word submitted!", "round": current_round})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
