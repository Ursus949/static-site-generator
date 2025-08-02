import unittest
from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()

