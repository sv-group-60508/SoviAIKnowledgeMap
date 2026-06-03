import os

root = "../sovi-20-questions-demo"
found = []
for dirpath, dirnames, filenames in os.walk(root):
    if any(x in dirpath for x in ["__pycache__", ".git", ".wrangler", "node_modules"]):
        continue
    for f in filenames:
        if f.endswith((".py", ".js", ".json", ".yaml", ".toml", ".vars", ".sh", ".md")):
            p = os.path.join(dirpath, f)
            try:
                with open(p, "r", encoding="utf-8") as file:
                    content = file.read()
                    if "gemini-3.1-flash-image" in content:
                        print(f"Found in: {p}")
                        found.append(p)
            except:
                pass
if not found:
    print("Not found in any files.")
