import requests
import base64
import json

# Your Local API URL
URL = "http://127.0.0.1:8000/detect"
FILE_NAME = "ai_sample_en.mp3" # Or "ai_sample_hi.mp3"
API_KEY = "HACKATHON_TEST_KEY" # Make sure this matches your main.py

def test_api():
    try:
        # 1. Encode MP3 to Base64 String
        with open(FILE_NAME, "rb") as f:
            b64_string = base64.b64encode(f.read()).decode('utf-8')

        # 2. Match Hackathon Input Format
        payload = {"audio_base64": b64_string}
        headers = {"Authorization": API_KEY, "Content-Type": "application/json"}

        # 3. Send Request
        print(f"Testing local API with {FILE_NAME}...")
        response = requests.post(URL, json=payload, headers=headers)

        # 4. Show Result
        print("Status:", response.status_code)
        print("Response:", json.dumps(response.json(), indent=4))

    except FileNotFoundError:
        print("Error: Run 'python create_sample.py' first!")

if __name__ == "__main__":
    test_api()