import os
import shutil
from page_generator import generate_page

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
    public_dst = os.path.join(base, "..", "public")
    content_md = os.path.join(base, "..", "content", "index.md")
    template_html = os.path.join(base, "..", "template.html")
    output_html = os.path.join(public_dst, "index.html")

    copy_static(static_src, public_dst)
    generate_page(content_md, template_html, output_html)

if __name__ == "__main__":
    main()
