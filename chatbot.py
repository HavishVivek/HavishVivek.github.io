from flask import Flask, request, jsonify
import faiss
import json
import torch
from transformers import pipeline
from sentence_transformers import SentenceTransformer

# Load Hugging Face OpenAI model (you can replace it with any OpenAI model from Hugging Face)
chat_model = pipeline("text-generation", model="gpt2")
# Load Sentence Transformer model for embedding search
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Load FAISS index and blog data
index = faiss.read_index("blog_index.faiss")
with open("blog_texts.json", "r", encoding="utf-8") as f:
    blog_texts = json.load(f)

app = Flask(__name__)

def find_relevant_blog(query):
    """Find the most relevant blog post using FAISS."""
    query_embedding = embed_model.encode([query], convert_to_numpy=True).astype("float32")
    _, indices = index.search(query_embedding, k=1)  # Get top 1 match
    return blog_texts[indices[0][0]]

def generate_response(prompt):
    """Generate a response using Hugging Face's OpenAI model."""
    response = chat_model(prompt, max_length=300, num_return_sequences=1)
    return response[0]["generated_text"]

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "Query is required"}), 400

    relevant_blog = find_relevant_blog(user_query)
    prompt = f"Answer based on this blog:\n\nTitle: {relevant_blog['title']}\nCategory: {relevant_blog['category']}\nContent:\n{relevant_blog['content']}\n\nUser: {user_query}\nAI:"

    response = generate_response(prompt)
    
    return jsonify({"answer": response, "source": f"{relevant_blog['category']}/{relevant_blog['title']}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)