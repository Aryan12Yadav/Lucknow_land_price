from openai import OpenAI
from app.config import settings


class LLMService:

    def __init__(self):
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=settings.NVIDIA_API_KEY
        )

    def generate_response(self, query: str, context_docs: list, memory_text: str):
        context = "\n".join(context_docs[:2])

        prompt = f"""
Tum ek simple aur strict property assistant ho.

Previous Conversation:
{memory_text}

Context:
{context}

User Query:
{query}

Rules:
- Sirf context ke basis par answer do
- Apni taraf se kuch isse related add kr skte ho pr precisely
- Try to make innovative answer
- Use small amount of reasoning ability
- Agar exact data na mile toh bolo "data available nahi hai"
- Hinglish me simple answer do
- No markdown, no bullet points

Format:

Agar data mil jaye:
→ "<location> me shop rate Rs X per sqm hai..."

Agar data na mile:
→ "<location> ka data available nahi hai.
Nearby areas ke rates:
<list from context>"
"""

        try:
            completion = self.client.chat.completions.create(
                model="deepseek-ai/deepseek-v3-0324",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=300
            )

            response = completion.choices[0].message.content
            response = response.strip()
            response = response.replace("**", "").replace("*", "")

            return response

        except Exception as e:
            return f"Error: {str(e)}"


llm_service = LLMService()