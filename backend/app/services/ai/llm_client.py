import os
from dotenv import load_dotenv
import google.generativeai as gai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
gai.configure(api_key=api_key)

model = gai.GenerativeModel(
    model_name = "models/gemini-2.0-flash-exp",
    generation_config={
        "temperature": 0.2,
        "response_mime_type": "application/json"
    }
)

def chat_json(system_prompt: str, user_prompt: str) -> str:
    """
    Send a prompt to the Gemini model and return the JSON response.
    """

    prompt=f"""
{system_prompt}

{user_prompt}
"""
    response = model.generate_content(prompt)
    return response.text