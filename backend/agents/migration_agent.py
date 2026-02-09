from backend.groq_client import ask_llm

def generate_migration_guide(old_docs: str, new_docs: str) -> str:
    prompt = f"""
Create a MIGRATION GUIDE in Markdown.

Explain:
- What changed
- What users need to update
- Breaking changes (if any)

OLD VERSION:
{old_docs}

NEW VERSION:
{new_docs}
"""
    return ask_llm(prompt)
