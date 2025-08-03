import os
from markdown_to_html import markdown_to_html_node
from pathlib import Path

def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No H1 header found")

def generate_page(from_path: str, template_path: str, dest_path: str, base_path='/'):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    html_node = markdown_to_html_node(md_content)
    html_content = html_node.to_html()
    title = extract_title(md_content)

    result = template_content.replace("{{ Title }}", title)\
                             .replace("{{ Content }}", html_content)\
                             .replace("{{ base_path }}", base_path)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(result)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path='/'):
    for entry in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(full_path) and entry.endswith(".md"):
            dest_file = os.path.join(dest_dir_path, "index.html")
            generate_page(full_path, template_path, dest_file, base_path)

        elif os.path.isdir(full_path):
            generate_pages_recursive(full_path, template_path, dest_path, base_path)

