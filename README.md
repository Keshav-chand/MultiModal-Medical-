# 🏥 Multimodal Medical Assistant

An AI-powered medical assistant that combines **skin condition diagnosis from images** with **natural language medical Q&A** — built end-to-end with RAG, CNNs, and production-grade deployment on AWS.

---

## Problem

Most people experiencing skin issues either self-diagnose incorrectly via Google or wait weeks for a dermatology appointment. Meanwhile, general medical Q&A tools like ChatGPT give generic answers not grounded in verified medical sources.

The gap: there was no tool that could **look at a skin image, identify the condition, and immediately explain it with sourced medical context** — all in one interaction.

This project is my attempt to close that gap.

---

## Approach

The assistant has two modes that work together:

**1. Image-based skin diagnosis**
- Trained a CNN on the HAM10000 dataset (10,000+ dermatoscopy images across 7 skin condition classes)
- User uploads a skin image → model predicts the condition → confidence score returned

**2. RAG-powered medical Q&A**
- Medical documents and condition descriptions indexed using FAISS vector store
- User query → semantic search retrieves relevant chunks → LangChain feeds context to LLM → grounded answer generated
- One-line treatment suggestion appended from retrieved medical source

**3. Multimodal fusion**
- Image diagnosis output feeds into the RAG pipeline as context
- So if the CNN predicts "Melanocytic Nevi", the RAG system automatically retrieves and explains that condition
- User gets: diagnosis + explanation + treatment suggestion in a single response

**Infrastructure:**
- Flask API backend
- Deployed on AWS EC2 for scalable access
- CI/CD pipeline with Jenkins + Trivy (security scanning on every build)
- Dockerized for consistent environments

---

## Iterations

**v1 — Text Q&A only**
Started with just a LangChain + FAISS RAG pipeline over scraped medical PDFs. Answers were good but the system couldn't handle image inputs at all. Realized this was half the problem solved.

**v2 — Added CNN, no fusion**
Trained the CNN separately on HAM10000. It worked well in isolation (~83% validation accuracy) but the two systems were completely disconnected — users had to use them separately, which felt clunky.

**v3 — Multimodal fusion**
Connected the CNN output to the RAG pipeline. The predicted label from the image now seeds the retrieval query automatically. This made the UX feel seamless — upload image, get a full explanation.

**v4 — Production deployment**
Moved from local Flask dev server to AWS EC2. Added Jenkins pipeline for automated builds and Trivy for container vulnerability scanning. This was a significant jump — had to debug EC2 security groups, IAM roles, and Docker networking issues I hadn't encountered before.

---

## Key Design Choices

**Why FAISS over a hosted vector DB?**
Speed and cost. For a prototype, FAISS runs in-memory with no external dependencies. It's fast enough for this use case and keeps the system self-contained.

**Why LangChain?**
The chain abstraction made it easy to swap LLMs and experiment with prompt templates without rewriting the retrieval logic. Also made the multimodal fusion step cleaner — the CNN label just becomes another input to the chain.

**Why Jenkins + Trivy instead of GitHub Actions?**
Wanted hands-on experience with self-hosted CI/CD. Trivy specifically because security scanning on medical AI tools matters — you don't want vulnerable dependencies in a health-related application.

**CNN architecture choice**
Used a transfer learning approach rather than training from scratch — fine-tuned a pretrained base on HAM10000. Medical imaging datasets are small relative to ImageNet-scale data, so transfer learning was the pragmatic choice.

---

## Daily Time Commitment

Available for **6-8 hours/day** during the internship period. I treat side projects like a job — I show up consistently, document decisions, and ship iteratively.

---

## Stack

`Python` `LangChain` `FAISS` `Flask` `CNN` `AWS EC2` `Docker` `Jenkins` `Trivy` `HAM10000`

---
## Architecture
<img width="1402" height="1084" alt="image" src="https://github.com/user-attachments/assets/2b81bd73-4a95-4844-9224-853ec6c23ac8" />


## Running Locally

```bash
git clone https://github.com/Keshav-Chand/multimodal-medical-assistant
cd multimodal-medical-assistant
pip install -r requirements.txt
python app.py
```

Upload a skin image or type a medical query at `http://localhost:5000`

