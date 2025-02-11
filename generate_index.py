import os
import json
import glob

# Define paths
docs_dir = "/data/docs/"
output_file = "/data/docs/index.json"

# Dictionary to store file-title mappings
index = {}

# Find all Markdown (.md) files
md_files = glob.glob(os.path.join(docs_dir, "**/*.md"), recursive=True)

# Extract H1 title from each file
for md_file in md_files:
    file_name = os.path.relpath(md_file, docs_dir)  # Remove /data/docs/ prefix
    with open(md_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line.startswith("# "):  # First H1 found
                index[file_name] = line[2:].strip()  # Extract title
                break

# Save the index to JSON
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(index, json_file, indent=4, ensure_ascii=False)

print("Markdown index successfully created at:", output_file)
