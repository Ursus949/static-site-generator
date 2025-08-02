import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq_simple(self):
        node1 = HTMLNode("p", "P1", None, {"href": "https://google.com"})
        node2 = HTMLNode("p", "P1", None, {"href": "https://google.com"})
        self.assertEqual(node1, node2)

    def test_eq_empty_nodes(self):
        node1 = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node1, node2)

    def test_not_eq_different_tag(self):
        node1 = HTMLNode("p", "P1")
        node2 = HTMLNode("div", "P1")
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_value(self):
        node1 = HTMLNode("p", "Hello")
        node2 = HTMLNode("p", "World")
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_props(self):
        node1 = HTMLNode("p", "P1", None, {"href": "https://google.com"})
        node2 = HTMLNode("p", "P1", None, {"href": "https://bing.com"})
        self.assertNotEqual(node1, node2)

    def test_not_eq_other_type(self):
        node = HTMLNode("p", "P1")
        self.assertNotEqual(node, "Not an HTMLNode")

    def test_props_to_html_single(self):
        node = HTMLNode("a", "Click", None, {"href": "https://google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode("a", "Click", None, {"href": "https://google.com", "target": "_blank"})
        props_str = node.props_to_html()
        self.assertIn('href="https://google.com"', props_str)
        self.assertIn('target="_blank"', props_str)

    def test_props_to_html_none(self):
        node = HTMLNode("p", "Hello")
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("p", "P1", None, {"href": "https://google.com"})
        repr_str = repr(node)
        self.assertIn("Tag=p", repr_str)
        self.assertIn("Value=P1", repr_str)
        self.assertIn("Props={'href': 'https://google.com'}", repr_str)

    def test_eq_with_children(self):
        child1 = HTMLNode("span", "Hello")
        child2 = HTMLNode("span", "Hello")
        parent1 = HTMLNode("div", None, [child1])
        parent2 = HTMLNode("div", None, [child2])
        self.assertEqual(parent1, parent2)

    def test_not_eq_with_children(self):
        child1 = HTMLNode("span", "Hello")
        child2 = HTMLNode("span", "World")
        parent1 = HTMLNode("div", None, [child1])
        parent2 = HTMLNode("div", None, [child2])
        self.assertNotEqual(parent1, parent2)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://google.com">Click me!</a>'
        )

    def test_leaf_to_html_bold(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_leaf_to_html_raw_text(self):
        node = LeafNode(None, "Just plain text.")
        self.assertEqual(node.to_html(), "Just plain text.")

    def test_leaf_to_html_with_multiple_props(self):
        node = LeafNode("span", "Styled", {"class": "highlight", "id": "s1"})
        html = node.to_html()
        # order not guaranteed, test presence
        self.assertIn('<span', html)
        self.assertIn('class="highlight"', html)
        self.assertIn('id="s1"', html)
        self.assertIn('>Styled</span>', html)

    def test_leaf_raises_without_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_mixed_leaf_and_text(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], props={"class": "wrapper", "id": "main"})
        html = parent.to_html()
        self.assertIn('<div', html)
        self.assertIn('class="wrapper"', html)
        self.assertIn('id="main"', html)
        self.assertIn('<span>child</span>', html)

    def test_raises_without_tag(self):
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [LeafNode("span", "text")])
        self.assertIn("requires a tag", str(context.exception))

    def test_raises_without_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", [])
        self.assertIn("requires at least one child", str(context.exception))

if __name__ == "__main__":
    unittest.main()

