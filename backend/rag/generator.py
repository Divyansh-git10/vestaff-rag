from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_answer(query, contexts):

    context = "\n\n".join(contexts)

    prompt = f"""
You are an AI assistant answering questions ONLY from the AWS Customer Agreement.

Rules:
1. Use only the provided context.
2. If answer is not present in the context, reply:
   "The answer is not available in the document."
3. Do not make up information.

Context:
{context}

Question:
{query}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content