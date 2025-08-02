import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq_identical_nodes(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq_with_url(self):
        node1 = TextNode("Click here", TextType.LINK, "https://example.com")
        node2 = TextNode("Click here", TextType.LINK, "https://example.com")
        self.assertEqual(node1, node2)

    def test_noteq_different_text(self):
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Goodbye", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_noteq_different_text_type(self):
        node1 = TextNode("Same text", TextType.TEXT)
        node2 = TextNode("Same text", TextType.CODE)
        self.assertNotEqual(node1, node2)

    def test_noteq_different_url(self):
        node1 = TextNode("Click", TextType.LINK, "https://a.com")
        node2 = TextNode("Click", TextType.LINK, "https://b.com")
        self.assertNotEqual(node1, node2)

    def test_noteq_none_url_vs_url(self):
        node1 = TextNode("Image", TextType.IMAGE)
        node2 = TextNode("Image", TextType.IMAGE, "https://img.com/pic.png")
        self.assertNotEqual(node1, node2)

    def test_repr_without_url(self):
        node = TextNode("Hello", TextType.TEXT)
        expected = "TextNode('Hello', text, None)"
        self.assertEqual(repr(node), expected)

    def test_repr_with_url(self):
        node = TextNode("Click me", TextType.LINK, "https://example.com")
        expected = "TextNode('Click me', link, https://example.com)"
        self.assertEqual(repr(node), expected)

    def test_eq_type_check(self):
        node = TextNode("Text", TextType.TEXT)
        not_a_node = "Not a TextNode"
        self.assertNotEqual(node, not_a_node)

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {})

    def test_bold(self):
        node = TextNode("bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold")

    def test_italic(self):
        node = TextNode("italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic")

    def test_code(self):
        node = TextNode("code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code")

    def test_link(self):
        node = TextNode("click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, "https://img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://img.png", "alt": "alt text"})

    def test_invalid_type(self):
        node = TextNode("weird", "unknown-type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_missing_url_for_link(self):
        node = TextNode("link", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_missing_url_for_image(self):
        node = TextNode("image", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()
