from pymongo import MongoClient
from datetime import datetime
from app.config import settings


class MongoService:

    def __init__(self):
        self.client = MongoClient(settings.MONGO_URI)
        self.db = self.client["chatbot_db"]
        self.collection = self.db["chat_history"]

    def save_chat(self, user_id: str, query: str, response: str):
        doc = {
            "user_id": user_id,
            "query": query,
            "response": response,
            "timestamp": datetime.utcnow()
        }
        self.collection.insert_one(doc)

    def get_chat_history(self, user_id: str, limit: int = 5):
        chats = list(
            self.collection
            .find({"user_id": user_id}, {"_id": 0})
            .sort("timestamp", -1)
            .limit(limit)
        )
        return chats[::-1]

    def format_memory(self, chats):
        memory = ""
        for chat in chats:
            memory += f"User: {chat['query']}\n"
            memory += f"Assistant: {chat['response']}\n\n"
        return memory


mongo_service = MongoService()