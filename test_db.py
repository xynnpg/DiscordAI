#!/usr/bin/env python3
"""
Test database connection and models
"""

import os
from dotenv import load_dotenv
from flask_web import create_app
from database import db, AIModel

def test_database():
    """Test database connection and models"""
    print("🔍 Testing database connection...")
    
    # Load environment variables
    load_dotenv()
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        try:
            # Test database connection
            print("✅ Database connection successful")
            
            # Get all models
            all_models = AIModel.query.all()
            print(f"📊 Total models in database: {len(all_models)}")
            
            # Get active models
            active_models = AIModel.query.filter_by(is_active=True).all()
            print(f"✅ Active models: {len(active_models)}")
            
            # Print model details
            for model in all_models:
                print(f"  • {model.name} (Active: {model.is_active})")
                print(f"    Official Name: {model.official_name}")
                print(f"    API Key: {model.api_key[:20]}...")
                print(f"    Created: {model.created_at}")
                print()
            
            return True
            
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False

if __name__ == "__main__":
    test_database() 