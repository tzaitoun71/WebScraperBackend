from flask import Flask, request, jsonify
from models import db, VisitorClassification
from scraping import scrape_website
from question_generator import classify_content, generate_questions
from visitor_categorization import categorize_user_profile
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

@app.post('/classify')
def classify():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "URL is required"}), 400

    scraped_content = scrape_website(url)
    industry_classification = classify_content(scraped_content)
    questions = generate_questions(industry_classification)

    return jsonify({
        "classification": industry_classification,
        "questions": questions
    })

@app.post('/categorize-visitor')
def categorize_visitor():
    data = request.json
    url = data.get('url')
    name = data.get('name')
    industry = data.get('industry')
    questions = data.get('questions')
    responses = data.get('responses')

    if not name or not url or not industry or not questions or not responses:
        return jsonify({"error": "Name, URL, industry, questions, and responses are required"}), 400

    visitor_profile = categorize_user_profile(industry, questions, responses)

    # Save everything to the database only after categorization is done
    visitor = VisitorClassification(
        name=name,
        url=url,
        industry_classification=industry,
        visitor_categorization=visitor_profile
    )
    db.session.add(visitor)
    db.session.commit()

    return jsonify({
        "visitor_profile": visitor_profile,
        "message": "Visitor data saved successfully"
    })

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
