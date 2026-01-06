import re
import os

# Configuration
INPUT_FILE = "index.html"
SRC_DIR = "src"
CSS_DIR = os.path.join(SRC_DIR, "css")
JS_DIR = os.path.join(SRC_DIR, "js")

# Ensure directories exist
os.makedirs(CSS_DIR, exist_ok=True)
os.makedirs(JS_DIR, exist_ok=True)

def extract_and_replace(content, tag, attr, file_ext, out_dir, comment_style):
    """
    Finds blocks like <script id="main">...</script>, 
    saves content to file, and replaces text with an include marker.
    """
    # Regex to find tags with specific IDs
    # Captures: 1=ID, 2=Content
    pattern = re.compile(
        f'<{tag}[^>]*{attr}="([^"]+)"[^>]*>(.*?)</{tag}>', 
        re.DOTALL | re.IGNORECASE
    )

    def replacer(match):
        block_id = match.group(1)
        block_content = match.group(2)
        
        # Clean up leading/trailing newlines
        block_content = block_content.strip("\n")
        
        filename = f"{block_id}.{file_ext}"
        filepath = os.path.join(out_dir, filename)
        
        # Save to file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(block_content)
        
        print(f"Extracted {filename}")
        
        # Return the tag with the include marker inside
        if comment_style == "js":
            marker = f"// #INCLUDE: {file_ext}/{filename}"
        else:
            marker = f"/* #INCLUDE: {file_ext}/{filename} */"
            
        return f'<{tag} id="{block_id}">\n{marker}\n</{tag}>'

    return pattern.sub(replacer, content)

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    print(f"Reading {INPUT_FILE}...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        full_text = f.read()

    # 1. Extract CSS (<style id="...">)
    full_text = extract_and_replace(
        full_text, "style", "id", "css", CSS_DIR, "css"
    )

    # 2. Extract JS (<script id="...">)
    full_text = extract_and_replace(
        full_text, "script", "id", "js", JS_DIR, "js"
    )

    # 3. Save the Skeleton HTML
    template_path = os.path.join(SRC_DIR, "index_template.html")
    with open(template_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    
    print(f"Done! Skeleton saved to {template_path}")
    print("You can now edit files in src/js and src/css")

if __name__ == "__main__":
    main()