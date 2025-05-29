from supabase import create_client
import requests
import os
from pypdf import PdfReader
from docx import Document as DocxDocument
import tiktoken

# Supabase client
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# Chunking logic (~300 tokens)
def split_text(text, max_tokens=380):
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    words = text.split(" ")
    chunks, current = [], ""

    for sentence in words:
        if len(enc.encode(current + sentence)) < max_tokens:
            current += sentence + " "
        else:
            chunks.append(current.strip())
            current = sentence + " "
    if current:
        chunks.append(current.strip())
    return chunks

# Ollama embedding call
def get_embedding(text):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text}
    )
    try:
        data = response.json()
    except Exception as e:
        print("[Embedding API] Could not parse JSON response:", response.text)
        raise
    if "embedding" not in data:
        print("[Embedding API] No 'embedding' key in response:", data)
        raise KeyError("'embedding' not in response from Ollama API")
    return data["embedding"]

# Handle PDF/DOCX/TXT input
def extract_text_from_file(filename):
    if filename.endswith(".pdf"):
        reader = PdfReader(filename)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif filename.endswith(".docx"):
        doc = DocxDocument(filename)
        return "\n".join([p.text for p in doc.paragraphs])
    elif filename.endswith(".txt"):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Unsupported file type: must be .pdf, .docx, or .txt")

# Embed & store
def embed_and_upload(filename):
    content = extract_text_from_file(filename)
    chunks = split_text(content)


    for chunk in chunks:
        # Remove null bytes (\u0000) from chunk to avoid DB errors
        clean_chunk = chunk.replace('\u0000', '')
        embedding = get_embedding(clean_chunk)
        supabase.table("documents").insert({
            "content": clean_chunk,
            "embedding": embedding,
            "source": filename
        }).execute()

    print(f"✅ Uploaded {len(chunks)} chunks from {filename} to Supabase.")


# --- RAG Chat Pipeline ---
import numpy as np

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def fetch_all_chunks():
    # Fetch all chunks and their embeddings from Supabase
    res = supabase.table("documents").select("content,embedding").execute()
    return res.data

def find_top_k_similar_chunks(query_embedding, k=3):
    import ast
    chunks = fetch_all_chunks()
    scored = []
    for chunk in chunks:
        embedding = chunk["embedding"]
        # If embedding is a string (e.g., "[0.1, 0.2, ...]"), parse it
        if isinstance(embedding, str):
            try:
                embedding = ast.literal_eval(embedding)
            except Exception:
                embedding = []
        # If embedding is a list of strings, convert to floats
        if isinstance(embedding, list) and len(embedding) > 0 and isinstance(embedding[0], str):
            try:
                embedding = [float(x) for x in embedding]
            except Exception:
                embedding = []
        score = cosine_similarity(query_embedding, embedding)
        scored.append((score, chunk["content"]))
    scored.sort(reverse=True)
    return [content for score, content in scored[:k]]

def ask_llm_with_context(question, context_chunks):
    prompt = (
        "Use the following context to answer the question.\n\n"
        "Context:\n"
        + "\n---\n".join(context_chunks)
        + f"\n\nQuestion: {question}\nAnswer:"
    )
    import json
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "gemma3:latest", "prompt": prompt},
        stream=True
    )
    full_response = ""
    try:
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    full_response += data["response"]
    except Exception as e:
        print("[LLM API] Error while streaming response:", e)
        raise
    return full_response

def rag_chat(question, k=3):
    query_embedding = get_embedding(question)
    top_chunks = find_top_k_similar_chunks(query_embedding, k=k)
    answer = ask_llm_with_context(question, top_chunks)
    return answer

if __name__ == "__main__":
    # Step 1: Embed documents
    print("Embedding sigmabatch.pdf ...")
    embed_and_upload("sigmabatch.pdf")
    print("Embedding reference_docs/sample.txt ...")
    embed_and_upload("reference_docs/sample.txt")

    # Step 2: Simple CLI for RAG chat
    print("\nRAG Chatbot (type 'exit' to quit)")
    while True:
        user_question = input("You: ")
        if user_question.strip().lower() == "exit":
            break
        answer = rag_chat(user_question)
        print("Bot:", answer)
