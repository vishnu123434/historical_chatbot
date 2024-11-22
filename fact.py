from flask import Blueprint, jsonify
import mysql.connector

fact_blueprint = Blueprint('fact', __name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="history_db"
)

@fact_blueprint.route('/api/random_fact', methods=['GET'])
def get_random_fact():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT fact FROM facts ORDER BY RAND() LIMIT 1")
    fact = cursor.fetchone()
    return jsonify(fact)
