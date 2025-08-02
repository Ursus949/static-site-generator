import unittest
from textnode import TextNode, TextType

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
        node1 = TextNode("Hello", TextType.PLAIN)
        node2 = TextNode("Goodbye", TextType.PLAIN)
        self.assertNotEqual(node1, node2)

    def test_noteq_different_text_type(self):
        node1 = TextNode("Same text", TextType.PLAIN)
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
        node = TextNode("Hello", TextType.PLAIN)
        expected = "TextNode(Hello, plain, None)"
        self.assertEqual(repr(node), expected)

    def test_repr_with_url(self):
        node = TextNode("Click me", TextType.LINK, "https://example.com")
        expected = "TextNode(Click me, link, https://example.com)"
        self.assertEqual(repr(node), expected)

    def test_eq_type_check(self):
        node = TextNode("Text", TextType.PLAIN)
        not_a_node = "Not a TextNode"
        self.assertNotEqual(node, not_a_node)

if __name__ == "__main__":
    unittest.main()
