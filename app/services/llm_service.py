from openai import OpenAI
from app.config import settings


class LLMService:

    def __init__(self):
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=settings.NVIDIA_API_KEY,
            timeout=120.0  # 2 minute timeout
        )

    def generate_response(self, query: str, context_docs: list, memory_text: str):
        context = "\n".join(context_docs[:2])

        prompt = f"""
Tum ek simple property assistant ho.

Context:
{context}

Previous Conversation:
{memory_text}

User Query:
{query}

Rules:
- Sirf context ke basis par answer do
- Agar data na mile toh bolo "data available nahi hai"
- Hinglish me simple short answer do
- No markdown, no bullet points
"""

        try:
            full_response = ""

            stream = self.client.chat.completions.create(
                model="meta/llama-3.3-70b-instruct",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=150,   # Kam karo - fast response
                stream=True
            )

            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta is not None:
                    full_response += delta

            full_response = full_response.strip()
            full_response = full_response.replace("**", "").replace("*", "")

            return full_response

        except Exception as e:
            print(f"LLM ERROR: {str(e)}")
            return f"Error: {str(e)}"


llm_service = LLMService()