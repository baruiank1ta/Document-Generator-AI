def calculate_completeness(docs: dict) -> dict:
    required = ["api", "tutorial", "changelog", "migration"]
    score = 0

    for key in required:
        if docs.get(key):
            score += 25

    return {
        "completeness_score": score,
        "missing": [k for k in required if not docs.get(k)]
    }
