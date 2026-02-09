from backend.groq_client import ask_llm

def generate_changelog(old_docs: str, new_docs: str) -> str:
    prompt = f"""
You are a release manager.

Generate a CHANGELOG in Markdown with sections:
- Added
- Changed
- Removed

OLD VERSION DOCS:
{old_docs}

NEW VERSION DOCS:
{new_docs}
"""
    return ask_llm(prompt)
