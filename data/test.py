import os
from dotenv import load_dotenv
from google import genai
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in .env file.")
    exit()

# 3. Initialize the Gemini 3 Pro client
client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-1.5-flash", 
        contents="Successfully loaded API key from env. Give me a quick 'Hello World'."
    )
    print("✅ System Check:")
    print(response.text)
except Exception as e:
    print(f"❌ API Error: {e}")