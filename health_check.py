#!/usr/bin/env python3
"""
Railway-compatible health check script
"""

import os
import sys

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['DISCORD_BOT_TOKEN']
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        return False

    print("✅ Required environment variables are set")
    return True

def check_database():
    """Check if database can be accessed"""
    try:
        from flask_web import create_app
        from database import db, AIModel

        app = create_app()
        with app.app_context():
            # Try to query the database
            model_count = AIModel.query.count()
            print(f"✅ Database accessible ({model_count} models)")
            return True

    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False

def main():
    """Main health check function for Railway"""
    print("🔍 Railway Health Check")
    print("-" * 30)

    # Check environment
    env_ok = check_environment()

    # Check database
    db_ok = check_database()

    print("-" * 30)
    if env_ok and db_ok:
        print("✅ Health check passed!")
        sys.exit(0)
    else:
        print("❌ Health check failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
