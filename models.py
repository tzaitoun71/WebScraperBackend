from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class VisitorClassification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)  
    url = db.Column(db.String, nullable=False)  
    industry_classification = db.Column(db.String, nullable=False)  
    visitor_categorization = db.Column(db.String, nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.now)
