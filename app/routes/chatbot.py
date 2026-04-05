from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag_service import rag_service
from app.services.llm_service import llm_service
from app.services.db_service import mongo_service

router = APIRouter()


class ChatRequest(BaseModel):
    user_id: str
    query: str


class ChatResponse(BaseModel):
    response: str


greeting_queries = ["hi", "hello", "hey", "good morning", "good evening"]
help_queries = ["what can you do", "help", "guide me"]
memory_queries = ["what did you say before", "previous answer", "last response", "repeat that", "again please"]
exit_queries = ["bye", "goodbye", "exit", "stop"]


def detect_intent(query):
    q = query.lower()
    if any(k in q for k in greeting_queries):
        return "greeting"
    if any(k in q for k in help_queries):
        return "help"
    if any(k in q for k in memory_queries):
        return "memory"
    if any(k in q for k in exit_queries):
        return "exit"
    return "rag"


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    user_id = request.user_id
    query = request.query
    intent = detect_intent(query)

    chats = mongo_service.get_chat_history(user_id, limit=5)
    memory_text = mongo_service.format_memory(chats)

    if intent == "greeting":
        return {"response": "Aryan here. Hello. Main aapki property related queries me help kar sakta hoon. Aap kya jaanna chahte ho"}

    if intent == "help":
        return {"response": "Aryan here. Main aapko property rates, nearby areas aur investment related suggestions de sakta hoon. Aap apni query batao"}

    if intent == "memory":
        if chats:
            last_chat = chats[-1]
            return {"response": f"Aryan here. Last time maine yeh bola tha: {last_chat['response']}"}
        else:
            return {"response": "Aryan here. Abhi tak koi previous chat nahi hai"}

    if intent == "exit":
        return {"response": "Aryan here. Thanks for visiting. Agar future me koi help chahiye ho to zaroor batana"}

    context_docs = rag_service.search(query)
    response = llm_service.generate_response(query, context_docs, memory_text)
    response = f"Aryan here. {response} Agar aur help chahiye ho to batao"
    mongo_service.save_chat(user_id, query, response)

    return {"response": response}