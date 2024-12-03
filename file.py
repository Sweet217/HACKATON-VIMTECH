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

app = Flask(__name__)


def create_embedding(text):
    """
    Generates an embedding for the provided text using OpenAI's embedding model.

    Args:
        text (str): The input text to be embedded.

    Returns:
        list: A vector representing the embedding of the input text.
    """
    response = openai.embeddings.create(model="text-embedding-3-small", input=text)
    embedding = response.data[0].embedding
    return embedding


@app.route("/api/save-pdf-text", methods=["POST"])
def save_pdf_text():
    """
    Handles the endpoint to save text extracted from a PDF.
    - Generates an embedding for the text.
    - Hashes the text to create a unique identifier.
    - Stores the text, its embedding, and metadata in the Pinecone index.

    Returns:
        JSON Response:
        - 200 OK: Text saved successfully.
        - 400 Bad Request: Missing or invalid input.
        - 500 Internal Server Error: Error during processing.
    """
    try:
        # Extract data from the request
        data = request.json
        pdf_text = data.get("text", "")

        # Validate input
        if not pdf_text:
            return jsonify({"message": "Text is required."}), 400

        # Create embedding for the text
        embedding = create_embedding(pdf_text)

        # Handle possible embedding generation errors
        if isinstance(embedding, str):
            return jsonify({"message": f"Error creating embedding: {embedding}"}), 500

        # Generate a unique hash for the text
        pdf_text_hash = hashlib.md5(pdf_text.encode()).hexdigest()[:512]

        # Store the text and its embedding in Pinecone
        index.upsert([(pdf_text_hash, embedding, {"text": pdf_text})])

        # Return success response
        return jsonify({"message": "Text from PDF saved successfully"}), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"message": f"Error saving PDF text: {str(e)}"}), 500


@app.route("/api/query-allergies", methods=["POST"])
def query_allergies():
    """
    Handles the endpoint to query allergy information.
    - Fetches metadata for a patient from the Pinecone index.
    - Combines metadata with user query.
    - Uses OpenAI's chat model to process the query and generate a response.

    Returns:
        JSON Response:
        - 200 OK: Successfully processed the query.
        - 400 Bad Request: Missing or invalid input.
        - 500 Internal Server Error: Error during processing.
    """
    try:
        # Extract data from the request
        data = request.json
        query_text = data.get("query", "")
        patient_id = data.get("patient-id", "")

        # Validate input
        if not query_text or not patient_id:
            return jsonify({"message": "Query text and patient ID are required."}), 400

        # Fetch the patient metadata from Pinecone
        query_response = index.fetch(ids=[patient_id])

        allergy_info_list = []

        # Check if relevant metadata is present
        if "vectors" in query_response and patient_id in query_response["vectors"]:
            vector_data = query_response["vectors"][patient_id]
            metadata = vector_data.get("metadata", {})

            # Append allergy information if found
            if "text" in metadata and metadata["text"]:
                allergy_info_list.append(metadata["text"])

        # Fallback if no relevant information is found
        if not allergy_info_list:
            allergy_info_list.append("No relevant allergy information found.")

        # Prepare the prompt for OpenAI
        combined_prompt = f"Allergy Info: {allergy_info_list}\n\nQuery: {query_text}"

        # Configure request to OpenAI API
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": "Bearer API_KEY",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "o1-mini-2024-09-12",
            "messages": [{"role": "user", "content": combined_prompt}],
        }

        # Send the request to OpenAI
        response = requests.post(url, headers=headers, json=payload)

        # Process the response
        if response.status_code == 200:
            print(combined_prompt)
            data = response.json()
            answer = data["choices"][0]["message"]["content"].strip()
            return jsonify({"response": answer}), 200
        else:
            # Handle OpenAI API errors
            return (
                jsonify({"message": "Error from OpenAI API", "details": response.text}),
                response.status_code,
            )

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"message": f"Error processing query: {str(e)}"}), 500


# Run the Flask app in debug mode
if __name__ == "_main_":
    app.run(debug=True)
