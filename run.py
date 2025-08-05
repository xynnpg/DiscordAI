#!/usr/bin/env python3
"""
Discord AI Bot Startup Script
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
    required_vars = ['DISCORD_BOT_TOKEN', 'GUILD_ID']
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

def start_flask_app():
    """Start Flask app in a separate thread"""
    try:
        from flask_web import create_app
        app = create_app()
        
        # Initialize database
        with app.app_context():
            from database import db
            db.create_all()
            print("✅ Database initialized")
        
        # Get port from environment
        port = int(os.environ.get('PORT', 5000))
        
        print(f"🌐 Starting Flask app on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except Exception as e:
        print(f"❌ Error starting Flask app: {e}")
        sys.exit(1)

def start_discord_bot():
    """Start Discord bot"""
    try:
        from discord_bot import DiscordBot
        bot = DiscordBot()
        print("🤖 Starting Discord bot...")
        bot.run()
        
    except Exception as e:
        print(f"❌ Error starting Discord bot: {e}")
        # Don't exit here, let Flask continue running
        print("⚠️  Discord bot failed, but Flask app will continue")

def main():
    """Main startup function"""
    print("🤖 Starting Discord AI Bot...")
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    print("✅ Environment variables loaded")
    
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=start_flask_app, daemon=True)
    flask_thread.start()
    
    # Wait a bit for Flask to start
    print("⏳ Waiting for Flask app to start...")
    time.sleep(3)
    
    # Start Discord bot in main thread
    start_discord_bot()

if __name__ == "__main__":
    main() 