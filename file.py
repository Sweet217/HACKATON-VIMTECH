import openai
import pinecone
from pinecone import Pinecone, ServerlessSpec
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import os
import hashlib
import requests

openai.api_key = ""
pc = Pinecone(api_key="")

index = pc.Index("allergies-index-hackaton")

app = Flask(_name_)


def create_embedding(text):
    response = openai.embeddings.create(model="text-embedding-3-small", input=text)
    embedding = response.data[0].embedding
    return embedding


@app.route("/api/save-pdf-text", methods=["POST"])
def save_pdf_text():
    try:
        data = request.json
        pdf_text = data.get("text", "")

        if not pdf_text:
            return jsonify({"message": "Text is required."}), 400

        embedding = create_embedding(pdf_text)

        if isinstance(embedding, str):
            return jsonify({"message": f"Error creating embedding: {embedding}"}), 500
        pdf_text_hash = hashlib.md5(pdf_text.encode()).hexdigest()[:512]

        index.upsert([(pdf_text_hash, embedding, {"text": pdf_text})])

        return jsonify({"message": "Text from PDF saved successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Error saving PDF text: {str(e)}"}), 500


@app.route("/api/query-allergies", methods=["POST"])
def query_allergies():
    try:
        data = request.json
        query_text = data.get("query", "")
        patient_id = data.get("patient-id", "")

        if not query_text or not patient_id:
            return jsonify({"message": "Query text and patient ID are required."}), 400

        query_response = index.fetch(ids=[patient_id])

        allergy_info_list = []

        if "vectors" in query_response and patient_id in query_response["vectors"]:
            vector_data = query_response["vectors"][patient_id]
            metadata = vector_data.get("metadata", {})

            if "text" in metadata and metadata["text"]:
                allergy_info_list.append(metadata["text"])

        if not allergy_info_list:
            allergy_info_list.append("No relevant allergy information found.")

        combined_prompt = f"Allergy Info: {allergy_info_list}\n\nQuery: {query_text}"

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": "Bearer API_KEY",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "o1-mini-2024-09-12",
            "messages": [{"role": "user", "content": combined_prompt}],
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            print(combined_prompt)
            data = response.json()
            answer = data["choices"][0]["message"]["content"].strip()
            return jsonify({"response": answer}), 200
        else:
            return (
                jsonify({"message": "Error from OpenAI API", "details": response.text}),
                response.status_code,
            )

    except Exception as e:
        return jsonify({"message": f"Error processing query: {str(e)}"}), 500


if _name_ == "_main_":
    app.run(debug=True)
