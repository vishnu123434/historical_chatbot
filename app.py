from flask import Flask, render_template, jsonify
import mysql.connector
import random

app = Flask(__name__)

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="history_db"
    )


# Home route serving the main page
@app.route('/')
def home():
    return render_template('index.html')

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


# Route to fetch quiz topics
@app.route('/api/quiz_topics')
def get_quiz_topics():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT topic_id, topic_name FROM quiz_topics")  # Assuming `topic_id` and `topic_name` columns
    topics = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(topics)


if __name__ == '__main__':
    app.run(debug=True)
