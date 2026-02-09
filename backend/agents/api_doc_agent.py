from backend.groq_client import ask_llm

def generate_api_docs(code: str) -> str:
    prompt = f"""
Generate professional API documentation in Markdown.

Include:
1. Overview
2. Functions / Endpoints
3. Parameters
4. Example usage
5. Error handling

CODE:
{code}
"""
    return ask_llm(prompt)
