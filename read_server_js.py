import os

server_path = "../sovi-20-questions-demo/server.js"
if os.path.exists(server_path):
    print("Found server.js")
    with open(server_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, 1):
        if "gemini-3.1-flash-image" in line or "BASE_URL" in line or "image" in line.lower():
            # Print index and line
            print(f"Line {i:03d}: {line.rstrip()}")
else:
    print("server.js not found")
