from backend.groq_client import ask_llm

def generate_tutorial(code: str) -> str:
    prompt = f"""
Create a beginner-friendly tutorial in Markdown.
Explain the code step by step.

CODE:
{code}
"""
    return ask_llm(prompt)
