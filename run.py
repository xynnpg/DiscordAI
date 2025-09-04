#!/usr/bin/env python3
"""
Discord AI Bot - Railway Compatible Startup Script
Runs Flask web interface and Discord bot together
"""

import os
import sys
import time
import threading
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['DISCORD_BOT_TOKEN']
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in Railway dashboard.")
        return False

    return True

def setup_database():
    """Initialize database tables"""
    try:
        from flask_web import create_app
        from database import db

        app = create_app()
        with app.app_context():
            db.create_all()
            print("✅ Database initialized")
        return app
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return None

def start_discord_bot():
    """Start Discord bot in background thread"""
    def run_bot():
        try:
            from discord_bot import main as discord_main
            print("🤖 Starting Discord bot...")
            discord_main()
        except Exception as e:
            print(f"❌ Discord bot error: {e}")
            # Don't crash the whole application

    # Start Discord bot in daemon thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    return bot_thread

def main():
    """Main function for Railway deployment"""
    print("🚀 Starting Discord AI Bot with Memory...")

    # Check environment variables
    if not check_environment():
        sys.exit(1)

    # Initialize database and create Flask app
    app = setup_database()
    if not app:
        sys.exit(1)

    # Start Discord bot in background
    bot_thread = start_discord_bot()

    # Get port for Railway
    port = int(os.environ.get('PORT', 5000))

    print(f"🌐 Starting Flask web interface on port {port}")
    print("🤖 Discord bot starting in background...")
    print("🧠 Memory functionality enabled")

    # Start Flask app (this will block)
    try:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False,
            use_reloader=False  # Prevent double startup
        )
    except Exception as e:
        print(f"❌ Flask startup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
