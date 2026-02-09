import os
import requests
from dotenv import load_dotenv

load_dotenv()

SCALEDOWN_API_KEY = os.getenv("SCALEDOWN_API_KEY")

def compress_code(code: str) -> str:
    if not code.strip():
        return ""

    if not SCALEDOWN_API_KEY:
        # fallback if key missing
        return code[:4000]

    try:
        response = requests.post(
            "https://api.scaledown.ai/v1/compress",
            headers={
                "Authorization": f"Bearer {SCALEDOWN_API_KEY}",
                "Content-Type": "application/json"
            },
            json={"text": code},
            timeout=20
        )

        response.raise_for_status()
        return response.json().get("compressed_text", code[:4000])

    except Exception:
        # safe fallback
        return code[:4000]
