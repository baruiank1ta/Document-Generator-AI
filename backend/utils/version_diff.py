import os

def read_version_docs(version_path: str) -> str:
    content = []

    for file in ["api.md", "tutorial.md"]:
        file_path = os.path.join(version_path, file)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content.append(f"\n# {file}\n" + f.read())

    return "\n".join(content)
