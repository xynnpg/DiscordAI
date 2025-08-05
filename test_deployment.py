#!/usr/bin/env python3
"""
Quick deployment test script
"""

import requests
import time

def test_deployment():
    """Test if the deployment is working"""
    print("🚀 Testing Deployment...")
    print("=" * 50)
    
    # You'll need to replace this with your actual Railway URL
    base_url = "https://your-railway-app.railway.app"  # Replace with your URL
    
    print(f"Testing URL: {base_url}")
    print()
    
    # Test 1: Health endpoint
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    print()
    
    # Test 2: Login page
    print("2. Testing login page...")
    try:
        response = requests.get(f"{base_url}/login", timeout=10)
        if response.status_code == 200:
            print("✅ Login page accessible")
        else:
            print(f"❌ Login page failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Login page error: {e}")
    
    print()
    print("=" * 50)
    print("🎯 Next Steps:")
    print("1. Deploy the updated code to Railway")
    print("2. Visit your Railway URL")
    print("3. Login with password: Dmz_2009@@")
    print("4. Look for the blue play button (▶️) on each model card")
    print("5. Click the play button to test a model")
    print("6. Check Railway logs if anything doesn't work")

if __name__ == "__main__":
    test_deployment() 