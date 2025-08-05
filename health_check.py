#!/usr/bin/env python3
"""
Simple health check script for Railway deployment
"""

import os
import sys
import requests
import time

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['DISCORD_BOT_TOKEN', 'GUILD_ID']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    
    print("✅ All required environment variables are set")
    return True

def check_flask_app():
    """Check if Flask app is running"""
    try:
        port = int(os.environ.get('PORT', 5000))
        url = f"http://localhost:{port}/health"
        
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("✅ Flask app is running and healthy")
            return True
        else:
            print(f"❌ Flask app returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Flask app is not responding: {e}")
        return False

def main():
    """Main health check function"""
    print("🔍 Running health checks...")
    print("-" * 40)
    
    # Check environment
    env_ok = check_environment()
    
    # Check Flask app
    flask_ok = check_flask_app()
    
    print("-" * 40)
    if env_ok and flask_ok:
        print("✅ All health checks passed!")
        sys.exit(0)
    else:
        print("❌ Some health checks failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 