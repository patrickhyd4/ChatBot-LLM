Local RAG Chatbot: Chat with Your Documents 📚💬
✨ Project Overview
Unlock the power of your private documents with this intuitive Retrieval Augmented Generation (RAG) chatbot. This project provides a seamless way to interact with your personal knowledge base by combining a locally hosted Large Language Model (LLM) with cutting-edge embedding and retrieval techniques. Say goodbye to endless searching – simply ask your questions, and let the RAG chatbot provide insightful answers directly from your uploaded files. It's like having a dedicated assistant for your documents!

🌟 Features at a Glance
Versatile Document Ingestion: Effortlessly process your knowledge base from various formats, including PDF, DOCX, and TXT files.
Intelligent Text Chunking: Documents are automatically segmented into optimized chunks (approximately 380 tokens)  to ensure efficient embedding and precise retrieval, striking a balance between context and conciseness.
On-Premise Embeddings: Harness the power of Ollama's nomic-embed-text model  for local, privacy-preserving generation of text embeddings.
Robust Supabase Integration: Securely store your document chunks and their high-dimensional embeddings in a Supabase database, enabling rapid and scalable information retrieval.
Locally Hosted LLM: Power your conversations with a locally running Large Language Model, specifically leveraging the gemma3:latest model via Ollama  for responsive and intelligent interactions.
Semantic Search with Cosine Similarity: Employ advanced cosine similarity algorithms to accurately identify and retrieve the most semantically relevant document chunks based on your queries.
Context-Aware Responses: The LLM intelligently synthesizes information by receiving the most pertinent document chunks as context, ensuring answers are grounded, accurate, and highly relevant to your specific data.
User-Friendly CLI: Interact with your RAG chatbot through a straightforward and engaging command-line interface.
🛠️ Technologies Under the Hood
This project is built upon a robust stack of modern technologies:

Python: The core programming language orchestrating the entire RAG pipeline.
Supabase: Serves as the scalable backend for efficient storage and management of document content and their vector embeddings.
Ollama: Facilitates the seamless local execution of both the embedding model (nomic-embed-text) and the powerful LLM (gemma3:latest).
pypdf: Empowers the extraction of textual content from PDF documents.
python-docx: Enables robust text extraction from DOCX file formats.
tiktoken: Crucial for precise text tokenization and intelligent chunk sizing, ensuring optimal input for embedding models.
numpy: Provides essential numerical computing capabilities, particularly for the cosine similarity calculations.
python-dotenv: Securely manages environment variables for sensitive credentials.
requests: Handles the HTTP communication with the local Ollama API.
🚀 Getting Started
Follow these steps to set up and run your local RAG chatbot.

Prerequisites
Before diving in, make sure you have these essential tools ready:

Python 3.8+: Download and install Python if you haven't already.
Ollama Installation:
Visit ollama.com to download and install Ollama for your operating system.
Once installed, open your terminal and pull the necessary models:
Bash

ollama pull nomic-embed-text
ollama pull gemma3:latest
Supabase Project Setup:
Navigate to Supabase and create a new project.

Crucially, enable the pg_vector extension in your Supabase project (find it under Database -> Extensions).

Create a documents table with the following SQL schema. This table will house your document chunks and their embeddings:

SQL

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(768), -- 'nomic-embed-text' produces 768-dimensional embeddings.
    source TEXT
);
Installation Steps
Clone the Repository:
Begin by cloning this project to your local machine:

Bash

git clone https://github.com/your-username/your-repo-name.git # Replace with your actual repo URL
cd your-repo-name
 Create a Virtual Environment:
It's highly recommended to use a virtual environment to manage dependencies:

Bash

python -m venv venv
source venv/bin/activate # On Windows: `venv\Scripts\activate`
Install Dependencies:
Install all required Python packages from the requirements.txt file:

Bash

pip install -r requirements.txt
Configure Environment Variables:
Create a file named .env in the root directory of your project. Populate it with your Supabase credentials:

SUPABASE_URL="YOUR_SUPABASE_URL"
SUPABASE_KEY="YOUR_SUPABASE_ANON_KEY"
You can find your Supabase URL and Anon Key in your Supabase project settings under Project Settings -> API.

👩‍💻 How to Use
1. Embed and Upload Your Documents
Prepare your documents for the chatbot by embedding their content and uploading them to your Supabase database.

Place your .pdf, .docx, or .txt files into a designated reference_docs/ folder (or adjust paths in the script).

Run the embed_and_upload.py script. This script is configured to process sigmabatch.pdf and sample.txt by default. You can easily modify the if __name__ == "__main__": block within embed_and_upload.py to include other documents you wish to integrate.

Bash

python embed_and_upload.py
You will see progress messages as chunks are uploaded to Supabase.

2. Engage with Your Chatbot
Once your documents are embedded, you can start interacting with your RAG chatbot:

Bash

python embed_and_upload.py
The chatbot will launch in your terminal, prompting you to enter questions. Type your query and press Enter. To gracefully exit the conversation, simply type exit.

RAG Chatbot (type 'exit' to quit)
You: What is the duration of the Sigma Batch course?
Bot: The duration of the Sigma Batch course is 4.5 Months. [cite: 7]
You: Tell me about the MERN Stack development.
Bot: The MERN Stack development covers Complete Frontend Development, Complete Backend Development, Complete Database (SQL & MongoDB), and Complete MERN Stack (MongoDB, Express, React, Node). It also includes Real Life and Industry Grade Projects, LIVE sessions on how to get a job, resume, open source & more. [cite: 6]
You: exit
📂 Project Structure
.
├── embed_and_upload.py       # The heart of the project: handles document embedding, Supabase upload, and the RAG chat pipeline.
├── main.py                   # (Legacy/Example) A simpler, initial script for basic LLM interaction. The RAG pipeline is in embed_and_upload.py.
├── requirements.txt          # Lists all Python libraries required for the project.
├── .env                      # Stores sensitive environment variables (e.g., Supabase credentials).
├── sample.txt                # A sample text document for demonstration and testing the RAG pipeline. [cite: 2]
└── sigmabatch.pdf            # A sample PDF document (e.g., course details) used to showcase PDF text extraction and RAG capabilities. [cite: 3]
🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have suggestions for improving this project, please fork the repo and create a pull request. You can also open an issue with the tag "enhancement."

Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request
⚖️ License
Distributed under the [Your Chosen License] License. See the LICENSE file for more information.