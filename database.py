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

class ConversationHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    model_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Index for faster queries
    __table_args__ = (
        db.Index('idx_user_created', 'user_id', 'created_at'),
    )

    @staticmethod
    def get_user_history(user_id: str, limit: int = 10):
        """Get recent conversation history for a user"""
        return ConversationHistory.query.filter_by(user_id=user_id)\
            .order_by(ConversationHistory.created_at.desc())\
            .limit(limit).all()

    @staticmethod
    def add_message(user_id: str, role: str, content: str, model_name: str):
        """Add a new message to conversation history"""
        message = ConversationHistory(
            user_id=user_id,
            role=role,
            content=content,
            model_name=model_name
        )
        db.session.add(message)
        db.session.commit()
        return message

    @staticmethod
    def clear_user_history(user_id: str):
        """Clear all conversation history for a user"""
        ConversationHistory.query.filter_by(user_id=user_id).delete()
        db.session.commit()

    @staticmethod
    def get_conversation_context(user_id: str, limit: int = 10):
        """Get conversation history formatted for API calls"""
        history = ConversationHistory.get_user_history(user_id, limit)
        # Reverse to get chronological order (oldest first)
        history.reverse()

        messages = []
        for msg in history:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        return messages
