import requests
import zipfile
import io
import os

ALLOWED_EXTENSIONS = (".py", ".md", ".txt", ".yaml", ".yml")


def load_github_repo(repo_url: str) -> str:
    """
    Downloads a GitHub repository as a ZIP and extracts readable source files.
    """

    if repo_url.endswith("/"):
        repo_url = repo_url[:-1]

    # Convert GitHub repo URL to ZIP URL
    # https://github.com/user/repo -> https://github.com/user/repo/archive/refs/heads/main.zip
    zip_url = repo_url + "/archive/refs/heads/main.zip"

    response = requests.get(zip_url)

    if response.status_code != 200:
        raise Exception("Failed to download GitHub repository")

    extracted_code = []

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.lower().endswith(ALLOWED_EXTENSIONS):
                with zip_ref.open(file_name) as f:
                    try:
                        content = f.read().decode("utf-8", errors="ignore")
                        extracted_code.append(
                            f"\n\n# FILE: {file_name}\n\n{content}"
                        )
                    except Exception:
                        continue

    return "\n".join(extracted_code)
