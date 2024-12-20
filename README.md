# HACKATON-WIMTACH

Chatbot Personality and Data Integration Tools
This repository contains two distinct tools:

Chatbot Personality Simulator
A conversational application simulating interactions between two chatbots with predefined personalities.

Embedding-Based Data API
A Flask API for embedding text data and querying it using Pinecone and OpenAI's APIs.

Chatbot Personality and Data Integration Tools
This repository contains two distinct tools:

Chatbots Reacting to each other messages.
A conversational application simulating interactions between two chatbots with predefined personalities.

Chatbots Reacting to each other messages.
A Flask API for embedding text data and querying it using Pinecone and OpenAI's APIs.

1. Chatbot Personality Simulator
   Overview
   Simulates conversations between two chatbots:

Mom Agent: Overprotective and anxious mom interacting with a doctor.
Child Agent: A playful, casual 13-year-old Canadian child.
Features
Dual Personality Agents:
Mom: Displays caring yet overbearing behavior.
Child: Converses casually and playfully, expressing mild frustration at the mom's interruptions.
Interactive Conversations: Allows dynamic back-and-forth dialogues with agents.
OpenAI Integration: Generates responses using OpenAI's chat models.
How to Use
Set your OpenAI API key in the api_key variable.
Run the script and start the conversation loop.
Input queries, and observe how both agents respond based on their personalities.
Type exit to end the session. 2. Embedding-Based Data API
Overview
A RESTful API for:

Embedding text data using OpenAI.
Storing and querying data in Pinecone.
Managing structured allergy information.
Features
Save PDF Texts: Upload and embed PDF content for storage in Pinecone.
Query Allergy Data: Fetch and analyze allergy-related information for a given patient.
OpenAI-Powered Insights: Processes queries to generate detailed responses using OpenAI's chat models.
API Endpoints
POST /api/save-pdf-text
Save text from PDFs with embeddings into Pinecone. (We use medical registers.)

Request Body:
json
{ "text": "Your PDF text here" }

Response:
json
{ "message": "Text from PDF saved successfully" }
POST /api/query-allergies
Query allergy information for a patient.

Request Body:
json
{
"query": "Your query here",
"patient-id": "UniquePatientID"
}
Response:
json
{ "response": "Detailed response from OpenAI" }
Prerequisites
Python 3.8+
Installed dependencies (pip install -r requirements.txt):
openai
flask
pinecone-client
requests
Usage
Chatbot Personality Simulator
Run the script:
Interact with the agents in a simulated dialogue.

Embedding-Based Data API
Start the Flask server:
Use tools like Postman or curl to interact with the API.
Set up the following keys and tokens before running the scripts: The Api key.

OpenAI API Key: Replace api_key with your OpenAI key.
Pinecone API Key: Replace api_key in the Pinecone initialization.
