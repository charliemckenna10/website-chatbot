from flask import Flask, request, jsonify
from demo_chatbott import RealEstateBot
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

bot = RealEstateBot()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400

    user_message = data["message"]
    bot_response, leads = bot.chat(user_message)

    return jsonify({
        "response": bot_response,
        "leads": leads
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
