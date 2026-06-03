import os

file_path = "../sovi-20-questions-demo/pictures/generate_characters.py"
with open(file_path, "r") as f:
    lines = f.readlines()

start = 480
end = 510
for i in range(start, min(end, len(lines))):
    print(f"Line {i+1:03d}: {lines[i].rstrip()}")
