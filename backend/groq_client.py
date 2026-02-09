import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY missing in .env")

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "llama-3.1-8b-instant"

def ask_llm(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior technical writer who generates clean, professional documentation."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=600
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"LLM ERROR: {str(e)}"
