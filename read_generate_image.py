import os

server_path = "../sovi-20-questions-demo/server.js"
if os.path.exists(server_path):
    print("Found server.js")
    with open(server_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    for i in range(1499, min(1545, len(lines))):
        print(f"Line {i+1:03d}: {lines[i].rstrip()}")
