from flask import Flask, render_template, jsonify, request
import mysql.connector
import random

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="chatbot_db"
)
#Preprocessing queries

def preprocess_query(text):
    query=query.lower()
    query=re.sub(r'\s+', '', query)
    query=re.sub(r'[^a-zA-Z0-9\s]', '', query)
    return query.strip()

# Function to search the database for user queries
def search_in_db(query):
    cursor = db.cursor(dictionary=True)
    
    # Using SQL LIKE operator to match user query with the database content
    search_query = "SELECT content FROM history_data WHERE title LIKE %s OR content LIKE %s LIMIT 1"
    search_term = f"%{query}%"
    
    cursor.execute(search_query, (search_term, search_term))
    result = cursor.fetchone()
    
    if result:
        return result['content']  # Return the content if a match is found
    else:
        return None  # Return None if no match is found

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route to give a random fact
@app.route('/give_fact', methods=['GET'])
def give_fact():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT fact FROM facts ORDER BY RAND() LIMIT 1")
    fact = cursor.fetchone()
    return jsonify(fact)

# Route to take a random quiz
@app.route('/take_quiz', methods=['GET'])
def take_quiz():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM quiz ORDER BY RAND() LIMIT 1")
    quiz = cursor.fetchone()
    return jsonify(quiz)

# Chatbot route - search database for historical information
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.form['message']  # User message from the frontend
    
    # Search in the database first
    db_result = search_in_db(user_input)
    
    if db_result:
        # If relevant data is found in the database, return it
        return jsonify({'fact': db_result})
    else:
        # If no data found, respond accordingly
        return jsonify({'fact': "I'm sorry, I don't have information on that topic."})

if __name__ == '__main__':
    app.run(debug=True)
