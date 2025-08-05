from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True, nullable=False)
    model_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AIModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    official_name = db.Column(db.String(100), nullable=False)
    api_key = db.Column(db.String(500), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    team_only = db.Column(db.Boolean, default=False)  # New field for team-only mode
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 