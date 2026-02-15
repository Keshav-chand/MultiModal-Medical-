from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from app.components.retriever import create_qa_chain

load_dotenv()

app = Flask(__name__)
CORS(app)

qa_chain = None

def get_qa_chain():
    global qa_chain
    if qa_chain is None:
        print("🟢 Initializing QA chain (first request only)")
        qa_chain = create_qa_chain()
    return qa_chain


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"error": "Question is required"}), 400

    question = data["question"]

    try:
        chain = get_qa_chain()
        response = chain.invoke({"query": question})
        answer = response.get("result", "No response generated")
        return jsonify({"answer": answer})

    except Exception as e:
        print("🔴 ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

