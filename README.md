# ChatBot-LLM
in short, we are trying to make a chatbot that uses a privately hosted LLM with a RAG pipepline. The source of the RAG should be documents in a reference folder
Local RAG Chatbot
Project Overview
This project implements a Retrieval Augmented Generation (RAG) chatbot that allows you to interact with your private documents using a locally hosted Large Language Model (LLM) and embedding model. The core idea is to enhance the LLM's responses by providing relevant context extracted from your own document collection. This enables the chatbot to answer questions specific to your uploaded files, making it feel like you're "chatting with your documents."

Features
Document Ingestion: Supports PDF, DOCX, and TXT file formats for document ingestion. 
Text Chunking: Documents are automatically split into smaller chunks (approximately 300 tokens) to optimize for embedding and retrieval. 
Local Embeddings: Utilizes Ollama's nomic-embed-text model for generating embeddings locally. 
Supabase Integration: Stores document chunks and their embeddings in a Supabase database for efficient retrieval. 
Local LLM Integration: Leverages a locally hosted LLM (specifically gemma3:latest through Ollama) for generating responses. 
Cosine Similarity Search: Retrieves the most relevant document chunks based on cosine similarity to the user's query. 
Contextual Question Answering: The LLM receives the relevant document chunks as context to provide accurate and informed answers. 
Command-Line Interface (CLI): Simple CLI for interacting with the chatbot. 
Technologies Used
Python: Primary programming language.
Supabase: Backend for storing document chunks and embeddings.
Ollama: For locally running the embedding model (nomic-embed-text) and the LLM (gemma3:latest).
pypdf: For extracting text from PDF documents. 
python-docx: For extracting text from DOCX documents. 
tiktoken: For tokenizing text and managing chunk sizes. 
numpy: For numerical operations, specifically cosine similarity calculation. 
python-dotenv: For managing environment variables. 
requests: For making HTTP requests to the Ollama API. 
Setup and Installation
Prerequisites
Before you begin, ensure you have the following installed:

Python 3.8+
Ollama: Download and install Ollama from ollama.com.
After installation, pull the required models:
Bash

ollama pull nomic-embed-text
ollama pull gemma3:latest
Supabase Project:
Create a new Supabase project.

Enable the pg_vector extension in your Supabase project (Database -> Extensions -> search for vector and enable it).

Create a documents table with the following schema:

SQL

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(768), -- Adjust dimension based on your embedding model (nomic-embed-text is 768)
    source TEXT
);
Installation Steps
Clone the repository:

Bash

git clone <your-repository-url>
cd <your-repository-name>
Create a virtual environment (recommended):

Bash

python -m venv venv
source venv/bin/activate # On Windows: `venv\Scripts\activate`
Install dependencies:

Code snippet

pip install -r requirements.txt
Configure environment variables:

Create a .env file in the root directory of your project and add your Supabase credentials:

SUPABASE_URL="YOUR_SUPABASE_URL"
SUPABASE_KEY="YOUR_SUPABASE_ANON_KEY"
You can find these in your Supabase project settings (Settings -> API).

Usage
1. Embed and Upload Documents
To make your documents searchable by the chatbot, you need to embed their content and upload them to Supabase. The embed_and_upload.py script handles this. 

Place your .pdf, .docx, or .txt files in a designated folder (e.g., reference_docs/ as seen in the example).

Run the script:

Bash

python embed_and_upload.py
This script will process sigmabatch.pdf and reference_docs/sample.txt by default. You can modify the if __name__ == "__main__": block in embed_and_upload.py to include other files you wish to embed.

2. Start the Chatbot
After embedding your documents, you can start the RAG chatbot:

Bash

python embed_and_upload.py
(Note: The main.py seems to be an older, simplified version of the chatbot. embed_and_upload.py contains the full RAG pipeline and CLI.) 


The chatbot will prompt you to enter questions. Type your query and press Enter. To exit, type exit.

RAG Chatbot (type 'exit' to quit)
You: What is the duration of the Sigma Batch course?
Bot: The duration of the Sigma Batch course is 4.5 Months. [cite: 7]
You: Tell me about the MERN Stack development.
Bot: The MERN Stack development covers Complete Frontend Development, Complete Backend Development, Complete Database (SQL & MongoDB), and Complete MERN Stack (MongoDB, Express, React, Node). It also includes Real Life and Industry Grade Projects, LIVE sessions on how to get a job, resume, open source & more. [cite: 5]
You: exit
Project Structure
.
├── embed_and_upload.py       # Main script for embedding documents and running the RAG chatbot [cite: 1]
├── main.py                   # (Legacy) A simpler script for basic chatbot interaction [cite: 2]
├── requirements.txt          # Python dependencies [cite: 3]
├── .env                      # Environment variables (Supabase URL, Key)
├── sample.txt                # Example text document for RAG [cite: 4]
└── sigmabatch.pdf            # Example PDF document (course details) for RAG [cite: 6]
Contributing
Feel free to fork this repository, open issues, or submit pull requests.

License
[Choose and add a license, e.g., MIT, Apache 2.0, etc.]







