from backend.groq_client import ask_llm

def generate_readme(code: str, repo_name: str) -> str:
    prompt = f"""
You are a senior technical writer.

Generate a PROFESSIONAL README.md for a GitHub repository.

Rules:
- Make it user-friendly
- Do NOT invent features
- Assume this is an open-source project
- Write in clean Markdown

Include these sections EXACTLY:
1. Project Title
2. Description
3. Features
4. Tech Stack
5. Project Structure
6. Installation
7. Usage
8. Example
9. Limitations
10. Future Improvements

Repository name: {repo_name}

CODE CONTEXT:
{code}
"""
    return ask_llm(prompt)
