from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os
import traceback

# Core pipeline
from backend.scaledown_client import compress_code
from backend.agents.api_doc_agent import generate_api_docs
from backend.agents.tutorial_agent import generate_tutorial

# GitHub support
from backend.github_loader import load_github_repo

# Advanced features
from backend.agents.changelog_agent import generate_changelog
from backend.agents.migration_agent import generate_migration_guide
from backend.utils.version_diff import read_version_docs
from backend.utils.metrics import calculate_completeness
from backend.agents.readme_agent import generate_readme


load_dotenv()

app = FastAPI(title="Documentation Generator Agent")

# -----------------------------
# Request Models
# -----------------------------

class CodeInput(BaseModel):
    code: Optional[str] = None
    github_url: Optional[str] = None
    version: str


# -----------------------------
# Health Check
# -----------------------------

@app.get("/")
def health():
    return {"status": "running"}


# -----------------------------
# Generate Documentation
# -----------------------------

@app.post("/generate")
def generate_docs(input: CodeInput):
    try:
        # -------------------------------------------------
        # 1. Validate input
        # -------------------------------------------------
        if not input.code and not input.github_url:
            return {"error": "Provide either `code` or `github_url`"}

        # -------------------------------------------------
        # 2. Load code (GitHub OR raw code)
        # -------------------------------------------------
        if input.github_url:
            raw_code = load_github_repo(input.github_url)
        else:
            raw_code = input.code

        if not raw_code or not raw_code.strip():
            return {"error": "No valid source code found"}

        # -------------------------------------------------
        # 3. Compress code using ScaleDown
        # -------------------------------------------------
        compressed_code = compress_code(raw_code)

        # -------------------------------------------------
        # 4. Generate documentation using agents
        # -------------------------------------------------
        api_docs = generate_api_docs(compressed_code)
        tutorial = generate_tutorial(compressed_code)

        # 🔹 NEW: Extract repository name for README
        repo_name = "Project"
        if input.github_url:
            repo_name = input.github_url.rstrip("/").split("/")[-1]

        # 🔹 NEW: Generate README
        readme = generate_readme(compressed_code, repo_name)

        # -------------------------------------------------
        # 5. Save files in versioned folder
        # -------------------------------------------------
        docs_path = f"docs/{input.version}"
        os.makedirs(docs_path, exist_ok=True)

        with open(f"{docs_path}/README.md", "w", encoding="utf-8") as f:
            f.write(readme)

        with open(f"{docs_path}/api.md", "w", encoding="utf-8") as f:
            f.write(api_docs)

        with open(f"{docs_path}/tutorial.md", "w", encoding="utf-8") as f:
            f.write(tutorial)

        # -------------------------------------------------
        # 6. Return success response
        # -------------------------------------------------
            return {
                "status": "success",
                "version": input.version,
                "docs": {
                    "readme": readme,
                    "api": api_docs,
                    "tutorial": tutorial
                }
            }



    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }



# -----------------------------
# Compare Versions
# -----------------------------

@app.post("/compare")
def compare_versions(old_version: str, new_version: str):
    try:
        old_path = f"docs/{old_version}"
        new_path = f"docs/{new_version}"

        if not os.path.exists(old_path) or not os.path.exists(new_path):
            return {"error": "One or both versions do not exist"}

        old_docs = read_version_docs(old_path)
        new_docs = read_version_docs(new_path)

        changelog = generate_changelog(old_docs, new_docs)
        migration = generate_migration_guide(old_docs, new_docs)

        with open(f"{new_path}/CHANGELOG.md", "w", encoding="utf-8") as f:
            f.write(changelog)

        with open(f"{new_path}/MIGRATION.md", "w", encoding="utf-8") as f:
            f.write(migration)

        metrics = calculate_completeness({
            "api": True,
            "tutorial": True,
            "changelog": True,
            "migration": True
        })

        return {
            "status": "comparison complete",
            "metrics": metrics,
            "generated_files": [
                f"{new_path}/CHANGELOG.md",
                f"{new_path}/MIGRATION.md"
            ]
        }

    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
