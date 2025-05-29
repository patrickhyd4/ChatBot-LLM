from dotenv import load_dotenv
import os
from supabase import create_client
import requests

# Load .env values
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

print("SUPABASE_URL:", url)
print("SUPABASE_KEY (partial):", key[:6])  # Just to confirm it's loading

supabase = create_client(url, key)


def get_embedding(text):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text}
    )
    return response.json()["embedding"]


def query_gemma(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma3:latest",
            "prompt": prompt,
            "stream": False
        }
    )

    print("FULL RESPONSE JSON:", response.json())  # 🪵 Logs the full response

    return response.json().get("response", "❌ No 'response' key in JSON")


    print("FULL RESPONSE JSON:", response.json())  # 👈 Logs the full response

    return response.json().get("response", "❌ No 'response' key in JSON")


def chatbot_respond(user_query):
    query_embedding = get_embedding(user_query)
    # Dummy context for now — you will later fetch from Supabase
    context = "This is example content from your documents."
    prompt = f"Answer the question using the context below:\n\nContext:\n{context}\n\nQuestion: {user_query}\n\nAnswer:"
    return query_gemma(prompt)

if __name__ == "__main__":
    while True:
        q = input("You: ")
        print("Gemma:", chatbot_respond(q))
