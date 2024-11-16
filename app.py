from flask import Flask, render_template, jsonify
import mysql.connector
import random

# Specify the template folder here
app = Flask(__name__)

# Connect to the database
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",        # Database host
        user="root",    # Your MySQL username
        password="root", # Your MySQL password
        database="history_db"    # The name of your database
    )
    return connection

# Define the route for the homepage
@app.route('/')
def home():
    return render_template('index.html')  # Ensure 'index.html' is in the templates folder

# Define the route to get quiz topics
@app.route('/get_quiz_topics', methods=['GET'])
def get_quiz_topics():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT topic_id, topic_name FROM quiz_topics')
    topics = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(topics)

# Define the route for getting quiz questions from MySQL
@app.route('/get_quiz_questions/<topic_name>', methods=['GET'])
def get_quiz_questions(topic_name):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM quiz_questions WHERE topic_name = %s', (topic_name,))
    questions = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(questions)

# API route to fetch a random fact
@app.route('/api/random_fact', methods=['GET'])
def get_random_fact():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT fact FROM facts")
    facts = cursor.fetchall()
    
    if facts:
        random_fact = random.choice(facts)[0]  # Choose a random fact
    else:
        random_fact = "No facts available at the moment."  # Handle empty table

    cursor.close()
    conn.close()
    return jsonify({"fact": random_fact})


if __name__ == "__main__":
    app.run(debug=True,port=5001)

