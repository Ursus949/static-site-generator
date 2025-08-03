import os
import shutil
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
    public_dst = os.path.join(base, "..", "public")
    template_path = os.path.join(base, "..", "template.html")

    copy_static(static_src, public_dst)
    generate_pages_recursive(content_dir, template_path, public_dst)

if __name__ == "__main__":
    main()

