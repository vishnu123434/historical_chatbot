from flask import Blueprint, jsonify
import mysql.connector

quiz_blueprint = Blueprint('quiz', __name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="history_db"
)

@quiz_blueprint.route('/get_quiz_topics', methods=['GET'])
def get_quiz_topics():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT topic_id, topic_name FROM quiz_topics")
    topics = cursor.fetchall()
    return jsonify(topics)

@quiz_blueprint.route('/get_quiz_questions/<topic_name>', methods=['GET'])
def get_quiz_questions(topic_name):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM quiz_questions WHERE topic_name = %s", (topic_name,))
    questions = cursor.fetchall()
    return jsonify(questions)
