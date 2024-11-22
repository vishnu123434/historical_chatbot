from flask import Blueprint, request, jsonify
import re
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
from docx import Document

chatbot_blueprint = Blueprint('chatbot', __name__)

# Initialize Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load FAISS index and chunks
FAISS_DATA_DIR = "FAISS_DATA"

def load_faiss_index():
    try:
        index_path = os.path.join(FAISS_DATA_DIR, "historical_index.faiss")
        chunks_path = os.path.join(FAISS_DATA_DIR, "chunks.txt")

        index = faiss.read_index(index_path)
        with open(chunks_path, 'r', encoding='utf-8') as f:
            chunks = f.readlines()
        return index, chunks
    except Exception as e:
        print(f"Error loading FAISS index: {e}")
        return None, []

faiss_index, chunks = load_faiss_index()

# Preprocess query
def preprocess_query(text):
    query = text.lower()
    query = re.sub(r'[^a-zA-Z0-9\s]', '', query)
    return query.strip()

# Perform FAISS search
def search_faiss_index(user_query, top_k=1):
    if not faiss_index:
        return None
    query_embedding = np.array([model.encode(user_query)], dtype=np.float32)
    distances, indices = faiss_index.search(query_embedding, top_k)
    return [chunks[i] for i in indices[0] if i < len(chunks)]

# Load .docx files
DOCX_DIR = "ALL_DATA"

def load_docx_files():
    texts = []
    for file in os.listdir(DOCX_DIR):
        if file.endswith(".docx"):
            doc = Document(os.path.join(DOCX_DIR, file))
            texts.append('\n'.join([para.text for para in doc.paragraphs if para.text.strip()]))
    return texts

docx_texts = load_docx_files()

# Chatbot route
@chatbot_blueprint.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.form.get('message', '').strip()

    if not user_input:
        return jsonify({'response': "Please provide a valid query."})

    processed_input = preprocess_query(user_input)

    # Search in .docx files
    for doc in docx_texts:
        if processed_input in preprocess_query(doc):
            return jsonify({'response': doc})

    # Fall back to FAISS search
    faiss_results = search_faiss_index(user_input)
    response = faiss_results[0] if faiss_results else "No results found. Try rephrasing your query."
    return jsonify({'response': response})
