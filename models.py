from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class VisitorClassification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    classification = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)