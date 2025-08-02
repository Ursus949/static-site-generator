# 🛠️ Static Site Generator

A simple Python-based static site generator that parses inline Markdown and renders it as clean, semantic HTML using a custom data model.

---

## ✨ Features

- ✅ Inline Markdown to HTML conversion
  - **Bold**, *italic*, `code`, [links](#), and ![images](#)
- ✅ HTML AST model via `HTMLNode` trees
- ✅ Inline content model via `TextNode` objects
- ✅ Full test suite (no external test framework required)
- ✅ Shell scripts to run and test easily

---

## 📁 Project Structure

```
static-site-generator/
├── main.sh                      # 
├── test.sh                      # Runs all test files
└── src/
    ├── htmlnode.py              # Tree-based HTML node class
    ├── inline_markdown.py       # Markdown-to-TextNode parser
    ├── main.py                  # 
    ├── textnode.py              # Represents inline semantic content
    ├── test_htmlnode.py         # Unit tests for HTMLNode
    ├── test_inline_markdown.py  # Tests for Markdown parsing
    └── test_textnode.py         # Tests for TextNode & rendering
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Ursus949/static-site-generator.git
cd static-site-generator
```

### 2. Run the parser demo

```bash
./main.sh
```

### 3. Run all tests

```bash
./test.sh
```

> ⚠️ Requires Python 3.7+

---

## 🧪 Example Markdown Parsed

Input:
```markdown
This is **bold**, *italic*, and a [link](https://example.com).
```

Output (parsed structure):
```python
[
  TextNode("This is ", "text"),
  TextNode("bold", "bold"),
  TextNode(", ", "text"),
  TextNode("italic", "italic"),
  TextNode(", and a ", "text"),
  TextNode("link", "link", "https://example.com"),
  TextNode(".", "text"),
]
```

---

## 📦 Dependencies

No external packages required — 100% Python standard library.

---

## 📚 Future Ideas

- [ ] Todo

---

## 👤 Author

Made with ❤️ by Ursus949.

---

