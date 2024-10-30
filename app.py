from flask import Flask, request, jsonify
from models import db, VisitorClassification
from scraping import scrape_website
from question_generator import generate_content_based_questions
from visitor_categorization import determine_visitor_intent
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.post('/scrape')
def scrape():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    scraped_content = scrape_website(url)
    return jsonify({"content": scraped_content})

@app.post('/generate-questions')
def generate_questions():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "URL is required"}), 400

    scraped_content = scrape_website(url)
    questions = generate_content_based_questions(scraped_content)

    return jsonify({
        "questions": questions
    })

@app.post('/categorize-visitor')
def categorize_visitor():
    data = request.json
    url = data.get('url')
    name = data.get('name')
    questions = data.get('questions')
    responses = data.get('responses')

    if not name or not url or not questions or not responses:
        return jsonify({"error": "Name, URL, questions, and responses are required"}), 400

    visitor_intent = determine_visitor_intent(questions, responses)

    visitor = VisitorClassification(
        name=name,
        url=url,
        visitor_intent=visitor_intent
    )
    db.session.add(visitor)
    db.session.commit()

    return jsonify({
        "visitor_intent": visitor_intent,
        "message": "Visitor intent saved successfully"
    })

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
