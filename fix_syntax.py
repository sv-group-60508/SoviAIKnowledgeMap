import os

path = '../sovi-20-questions-demo/pictures/generate_characters.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'url_match = re.search(' in line and 'text_part)' in line:
        lines[i] = '                url_match = re.search(r"""https?://[^\\s)\\]\'"]+""", text_part)\n'
        print("Replaced line:", i)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
