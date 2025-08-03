import os
import shutil
import sys
from page_generator import generate_pages_recursive

def copy_static(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)

    for entry in os.listdir(src):
        src_path = os.path.join(src, entry)
        dst_path = os.path.join(dst, entry)
        if os.path.isdir(src_path):
            copy_static(src_path, dst_path)
        else:
            shutil.copy(src_path, dst_path)
            print(f"Copied: {dst_path}")

def main():
    base = os.path.dirname(__file__)
    static_src = os.path.join(base, "..", "static")
    content_dir = os.path.join(base, "..", "content")
    docs_dst = os.path.join(base, "..", "docs")
    template_path = os.path.join(base, "..", "template.html")

    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_static(static_src, docs_dst)
    generate_pages_recursive(content_dir, template_path, docs_dst, base_path)

if __name__ == "__main__":
    main()

