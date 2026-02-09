import os

def read_repo(repo_path):
    print("READING FROM PATH:", os.path.abspath(repo_path))

    all_code = ""

    if not os.path.exists(repo_path):
        print("PATH DOES NOT EXIST")
        return ""

    for root, _, files in os.walk(repo_path):
        for file in files:
            print("FOUND FILE:", file)
            if file.endswith((".py", ".js", ".java")):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    all_code += f"\n\n# FILE: {file}\n"
                    all_code += f.read()

    return all_code
