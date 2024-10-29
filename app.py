from flask import Flask, request, jsonify
from models import db, VisitorClassification
from scraping import scrape_website
from question_generator import classify_content
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Define routes
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

    scraped_content = scrape_website(url)

    classification = classify_content(scraped_content)

    visitor = VisitorClassification(url=url, classification=classification)
    db.session.add(visitor)
    db.session.commit()

    return jsonify({"message": "Classification saved successfully", "classification": classification})

# Create tables within the application context
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
