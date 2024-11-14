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


@app.route('/api/quiz_questions/<int:topic_id>', methods=['GET'])
def get_quiz_questions(topic_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch questions for the selected topic
    cursor.execute("SELECT question_text, option_a, option_b, option_c, option_d, correct_answer FROM quiz_questions WHERE topic_id = %s", (topic_id,))
    quiz_questions = cursor.fetchall()
    
    # Close the connection
    cursor.close()
    conn.close()
    
    # Return the questions as JSON
    return jsonify(quiz_questions)

if __name__ == '__main__':
    app.run(debug=True)