import os

zshrc_path = os.path.expanduser("~/.zshrc")
if os.path.exists(zshrc_path):
    print("Found ~/.zshrc")
    with open(zshrc_path, "r") as f:
        for line in f:
            if any(x in line.upper() for x in ["BASE_URL", "GEMINI", "NEW_API", "API_KEY"]):
                # Clean and print
                print(line.strip())
else:
    print("~/.zshrc not found")
