from flask import Flask
from flask import Flask, render_template, jsonify, request
from chatbot import chatbot_blueprint
from fact import fact_blueprint
from quiz import quiz_blueprint

# Initialize Flask app
app = Flask(__name__)

# Register Blueprints
app.register_blueprint(chatbot_blueprint)
app.register_blueprint(fact_blueprint)
app.register_blueprint(quiz_blueprint)

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
