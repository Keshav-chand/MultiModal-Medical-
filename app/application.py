from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from app.components.retriever import create_qa_chain

from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch

load_dotenv()

app = Flask(__name__)
CORS(app)

# ---------------------------
# Label Mapping (IMPORTANT)
# ---------------------------
LABEL_MAPPING = {
    "mel": "Melanoma",
    "nv": "Melanocytic nevi",
    "bcc": "Basal cell carcinoma",
    "akiec": "Actinic keratosis",
    "vasc": "Vascular lesions",
    "df": "Dermatofibroma",
    "bkl": "Benign keratosis"
}

# ---------------------------
# Load RAG QA Chain (Lazy)
# ---------------------------
qa_chain = None

def get_qa_chain():
    global qa_chain
    if qa_chain is None:
        print("🟢 Initializing QA chain (first request only)")
        qa_chain = create_qa_chain()
    return qa_chain


# ---------------------------
# Load HAM10000 Pretrained Model
# ---------------------------
print("🟢 Loading Skin Disease Model...")

model_name = "ALM-AHME/beit-large-patch16-224-finetuned-Lesion-Classification-HAM10000-AH-60-20-20"

processor = AutoImageProcessor.from_pretrained(model_name)
image_model = AutoModelForImageClassification.from_pretrained(model_name)

image_model.eval()

print("✅ Skin Disease Model Loaded")


# ---------------------------
# Text Chat Route (RAG)
# ---------------------------
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

        return jsonify({
            "prediction": None,
            "confidence": None,
            "medical_analysis": answer
        })

    except Exception as e:
        print("🔴 ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


# ---------------------------
# Image Classification + RAG
# ---------------------------
@app.route("/api/predict-image", methods=["POST"])
def predict_image():

    if "image" not in request.files:
        return jsonify({"error": "Image file is required"}), 400

    file = request.files["image"]

    try:
        # 🔹 Preprocess image
        image = Image.open(file).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")

        # 🔹 Run model
        with torch.no_grad():
            outputs = image_model(**inputs)

        logits = outputs.logits
        probs = torch.nn.functional.softmax(logits, dim=-1)

        predicted_class_idx = probs.argmax().item()
        confidence = probs[0][predicted_class_idx].item()

        raw_label = image_model.config.id2label[predicted_class_idx]

        # 🔹 Convert to full disease name
        disease_name = LABEL_MAPPING.get(raw_label, raw_label)

        # 🔹 Call RAG using predicted disease
        chain = get_qa_chain()
        response = chain.invoke({"query": disease_name})
        medical_answer = response.get("result", "No medical information found")

        # 🔹 Optional Safety Disclaimer
        disclaimer = ""
        if confidence < 0.60:
            disclaimer = (
                "\n\n⚠️ Confidence is relatively low. "
                "Please consult a certified dermatologist for accurate diagnosis."
            )

        return jsonify({
            "prediction": disease_name,
            "confidence": round(confidence * 100, 2),
            "medical_analysis": medical_answer + disclaimer
        })

    except Exception as e:
        print("🔴 IMAGE ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


# ---------------------------
# Health Check
# ---------------------------
@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)