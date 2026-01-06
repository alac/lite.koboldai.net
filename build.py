import re
import os

# Configuration
TEMPLATE_FILE = os.path.join("src", "index_template.html")
OUTPUT_FILE = os.path.join("dist", "kobold_lite_custom.html")
SRC_DIR = "src"

def main():
    if not os.path.exists(TEMPLATE_FILE):
        print(f"Error: {TEMPLATE_FILE} not found. Did you run unpack.py?")
        return

    os.makedirs("dist", exist_ok=True)

    print("Building...")
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to look for markers like:
    # // #INCLUDE: js/main.js  OR  /* #INCLUDE: css/style.css */
    # It handles arbitrary spaces
    include_pattern = re.compile(
        r'(?://|/\*)\s*#INCLUDE:\s*([a-zA-Z0-9_\-\./]+)\s*(?:\*/)?'
    )

    def replacer(match):
        relative_path = match.group(1)
        full_path = os.path.join(SRC_DIR, relative_path)
        
        if os.path.exists(full_path):
            print(f"  Merging {relative_path}...")
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            print(f"  WARNING: File {full_path} not found!")
            return f"/* ERROR: {relative_path} NOT FOUND */"

    # Perform the merge
    new_content = include_pattern.sub(replacer, content)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Success! Built {OUTPUT_FILE}")

if __name__ == "__main__":
    main()