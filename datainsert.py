import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
from docx import Document
import os
from tqdm import tqdm

# Model for embeddings
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Error loading SentenceTransformer model: {e}")
    exit(1)

# Function to extract text from a .docx file
def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        full_text = [para.text for para in doc.paragraphs if para.text.strip()]
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

# Function to get data from .docx files
def fetch_data_from_docx(docx_directory):
    docx_data = []
    for filename in os.listdir(docx_directory):
        if filename.endswith(".docx"):
            file_path = os.path.join(docx_directory, filename)
            text = extract_text_from_docx(file_path)
            if text.strip():  # Skip empty documents
                docx_data.append(text)
    return docx_data

# Function to chunk text into smaller segments
def split_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

# Create FAISS index and save
def create_faiss_index(data):
    chunks = []
    for text in tqdm(data, desc="Splitting text into chunks"):
        chunks.extend(split_text(text))

    embeddings = model.encode(chunks, show_progress_bar=True)  # Show progress for embeddings
    embeddings = np.array(embeddings)
    
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Save the FAISS index and chunks
    output_dir = "FAISS_DATA"
    os.makedirs(output_dir, exist_ok=True)
    faiss.write_index(index, os.path.join(output_dir, "historical_index.faiss"))
    with open(os.path.join(output_dir, "chunks.txt"), "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk + "\n")
    
    print(f"FAISS index created with {len(chunks)} chunks.")

# Example usage to fetch data from .docx files and create FAISS index
docx_directory = "ALL_DATA"  # Replace with the directory containing your .docx files
data = fetch_data_from_docx(docx_directory)
if data:
    create_faiss_index(data)
else:
    print("No valid data found in .docx files.")
