#!/usr/bin/env python3
"""
Test script for web interface functionality
"""

import requests
import json

def test_web_interface():
    """Test the web interface endpoints"""
    base_url = "http://localhost:5000"  # Change this to your Railway URL
    
    print("🔍 Testing Web Interface...")
    print("=" * 50)
    
    # Test 1: Health endpoint
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    print()
    
    # Test 2: Debug endpoint
    print("2. Testing debug endpoint...")
    try:
        response = requests.get(f"{base_url}/test_debug")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("✅ Debug endpoint working")
                print(f"   Total models: {data['total_models']}")
                for model in data['models']:
                    print(f"   - {model['name']} (Active: {model['is_active']})")
            else:
                print(f"❌ Debug endpoint failed: {data['error']}")
        else:
            print(f"❌ Debug endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Debug endpoint error: {e}")
    
    print()
    
    # Test 3: Login page
    print("3. Testing login page...")
    try:
        response = requests.get(f"{base_url}/login")
        if response.status_code == 200:
            print("✅ Login page accessible")
        else:
            print(f"❌ Login page failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Login page error: {e}")
    
    print()
    print("=" * 50)
    print("🎯 Manual Testing Steps:")
    print("1. Visit your Railway URL")
    print("2. Login with password: Dmz_2009@@")
    print("3. Try clicking the test button (play icon) on a model")
    print("4. Check the browser console for any JavaScript errors")
    print("5. Check Railway logs for any Python errors")

if __name__ == "__main__":
    test_web_interface() 