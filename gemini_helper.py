import os

from google import genai

from database import knowledge_base_summary


MODEL_NAME = "gemini-2.5-flash-lite"


def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def build_prompt(user_query, chat_history=None):
    history_text = ""
    if chat_history:
        recent = chat_history[-6:]
        history_text = "\n".join(f"{item['role']}: {item['content']}" for item in recent)

    return f"""
You are AgroAid AI, an intelligent farmer assistance chatbot for a social impact project.
Give simple, practical, farmer-friendly answers. Avoid complex scientific language.
Use Indian farming context where suitable. Add a safety note when advice needs local expert confirmation.

Knowledge base summary:
{knowledge_base_summary()}

Recent conversation:
{history_text}

Farmer question:
{user_query}

Answer format:
- Start with a direct answer.
- Give 3 to 5 useful points.
- Keep the tone supportive and easy to understand.
"""


def ask_gemini(user_query, chat_history=None):
    client = get_gemini_client()
    if client is None:
        return None, "Gemini API key not configured."

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=build_prompt(user_query, chat_history)
        )
        text = getattr(response, "text", None)
        if not text:
            return None, "Gemini returned an empty response."
        return text.strip(), None
    except Exception as error:
        return None, str(error)
