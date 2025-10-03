"""
Standalone script to test Google Gemini API key
"""

import requests
import json

# Your Google Gemini API key
API_KEY = "AIzaSyDY0PoN8G1rVqtGc12bakA801vAzXk02D0"

def test_gemini_api():
    """Test if the Google Gemini API key works"""

    # Use gemini-2.5-flash (available model)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    # Simple test prompt
    data = {
        "contents": [{
            "parts": [{
                "text": "Say 'API key is working!' if you can read this."
            }]
        }]
    }

    print("Testing Google Gemini API key...")
    print(f"API Key: {API_KEY[:20]}...")
    print(f"Model: gemini-2.5-flash")
    print("\nSending request...\n")

    try:
        response = requests.post(url, headers=headers, json=data)

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            message = result['candidates'][0]['content']['parts'][0]['text']
            print(f"\n✅ SUCCESS! API key is working!")
            print(f"\nGemini's response: {message}")
            return True
        else:
            print(f"\n❌ ERROR! Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"\n❌ ERROR! Exception occurred:")
        print(f"{type(e).__name__}: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini_api()
