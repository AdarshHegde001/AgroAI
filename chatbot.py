from gemini_helper import ask_gemini
from utils import detect_intent, fallback_response


class AgroAidChatbot:
    def __init__(self):
        self.name = "AgroAid AI"

    def get_response(self, user_query, chat_history=None, use_gemini=True):
        if not user_query or not user_query.strip():
            return "Please type a farming question so I can help.", "Validation"

        if use_gemini:
            ai_response, error = ask_gemini(user_query, chat_history)
            if ai_response:
                return ai_response, "Gemini AI"
            fallback = fallback_response(user_query)
            return f"{fallback}\n\nNote: Gemini fallback used because {error}", "Knowledge Base Fallback"

        return fallback_response(user_query), "Knowledge Base"

    def classify_query(self, user_query):
        return detect_intent(user_query)
