#!/usr/bin/env python3
"""
Script to update database schema for team_only field
"""

from flask_web import create_app
from database import db, AIModel

def update_database():
    """Update database schema and set default values"""
    app = create_app()
    
    with app.app_context():
        try:
            # Get the database engine
            engine = db.engine
            
            # Check if team_only column already exists
            inspector = db.inspect(engine)
            columns = [col['name'] for col in inspector.get_columns('ai_model')]
            
            if 'team_only' not in columns:
                # Add the team_only column using raw SQL
                with engine.connect() as conn:
                    conn.execute(db.text("ALTER TABLE ai_model ADD COLUMN team_only BOOLEAN DEFAULT FALSE"))
                    conn.commit()
                print("✅ Added team_only column to ai_model table")
            else:
                print("✅ team_only column already exists")
            
            # Now we can safely query the models
            models = AIModel.query.all()
            updated_count = 0
            
            for model in models:
                if model.team_only is None:
                    model.team_only = False
                    updated_count += 1
                    print(f"✅ Updated model '{model.name}' with team_only = False")
            
            if updated_count > 0:
                db.session.commit()
                print(f"✅ Updated {updated_count} models with default team_only = False")
            
            # Show current models
            print("\n📋 Current models:")
            for model in AIModel.query.all():
                status = "Team Only" if model.team_only else "Everyone"
                active = "Active" if model.is_active else "Inactive"
                print(f"  • {model.name} - {active}, {status}")
                
        except Exception as e:
            print(f"❌ Error updating database: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    update_database() 