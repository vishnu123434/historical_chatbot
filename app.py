from flask import Flask, render_template, request, jsonify
import mysql.connector
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import re
from fact import fact_blueprint
from quiz import quiz_blueprint

# Initialize the Flask app
app = Flask(__name__)

# Load the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Global FAISS Index and data
faiss_index = None
indexed_data = None

# Connect to database
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="history_db"
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Build FAISS Index
def build_faiss_index():
    global faiss_index, indexed_data
    conn = connect_db()
    if not conn:
        print("Failed to connect to the database.")
        return
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT sub_heading, content FROM hist_data")
        data = cursor.fetchall()
        indexed_data = data
        embeddings = [model.encode(row['content']) for row in data]
        faiss_index = faiss.IndexFlatL2(embeddings[0].shape[0])
        faiss_index.add(np.array(embeddings))
    except mysql.connector.Error as err:
        print(f"Database query error: {err}")
    finally:
        cursor.close()
        conn.close()

# Query FAISS Index
def query_faiss_index(query, k=5):
    if not faiss_index:
        return []
    query_vector = model.encode(query)
    distances, indices = faiss_index.search(np.array([query_vector]), k)
    return [indexed_data[idx] for idx in indices[0]]

# Summarize Response by Complete Sentences
def summarize_response(results, max_length=200):
    combined_content = " ".join([res['content'] for res in results])
    sentences = re.split(r'(?<=[.!?]) +', combined_content)
    summary = ""
    for sentence in sentences:
        if len(summary) + len(sentence) <= max_length:
            summary += sentence + " "
        else:
            break
    return summary.strip()

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Flask Route for chat functionality
@app.route('/chat', methods=['POST'])
def chat():
    user_query = request.json.get('user_input', '')
    if not user_query:
        return jsonify({"response": "Please provide a valid query."})

    results = query_faiss_index(user_query)
    if not results:
        return jsonify({"response": "No relevant data found for your query."})

    response = summarize_response(results)
    return jsonify({"response": response})

# Register Blueprints
app.register_blueprint(fact_blueprint)
app.register_blueprint(quiz_blueprint)

if __name__ == '__main__':
    build_faiss_index()
    if faiss_index:
        print("FAISS index successfully built!")
    else:
        print("Failed to build FAISS index.")
    app.run(debug=True, port=5002)  
    
