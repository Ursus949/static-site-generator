import unittest
from textnode import TextNode, TextType
from inline_markdown import (
        extract_markdown_images,
        extract_markdown_links,
        split_nodes_delimiter,
        split_nodes_image,
        split_nodes_link,
        text_to_textnodes,
)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_code(self):
        nodes = [TextNode("Some `code` here", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_single_bold(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_single_italic(self):
        nodes = [TextNode("This is _italic_ text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_inline(self):
        nodes = [TextNode("Use `code` and **bold**", TextType.TEXT)]
        step1 = split_nodes_delimiter(nodes, "`", TextType.CODE)
        step2 = split_nodes_delimiter(step1, "**", TextType.BOLD)
        expected = [
            TextNode("Use ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(step2, expected)

    def test_non_text_node_passthrough(self):
        nodes = [TextNode("skip me", TextType.LINK)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, nodes)

    def test_unmatched_delimiter_raises(self):
        nodes = [TextNode("This is **not closed", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

    def test_empty_segment_ignored(self):
        nodes = [TextNode("text `` empty", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("text ", TextType.TEXT),
            TextNode(" empty", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

class TestMarkdownExtraction(unittest.TestCase):

    def test_extract_markdown_images_single(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_multiple(self):
        text = "Text ![one](url1) more text ![two](url2)"
        expected = [("one", "url1"), ("two", "url2")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_none(self):
        text = "No images here!"
        self.assertListEqual(extract_markdown_images(text), [])

    def test_extract_markdown_links_single(self):
        text = "Here's a link [to Google](https://google.com)"
        expected = [("to Google", "https://google.com")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_multiple(self):
        text = "[GitHub](https://github.com) and [Docs](https://docs.example.com)"
        expected = [("GitHub", "https://github.com"), ("Docs", "https://docs.example.com")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_ignores_images(self):
        text = "![alt](image.png) and [link](url.com)"
        expected = [("link", "url.com")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_none(self):
        text = "Plain text with no links."
        self.assertListEqual(extract_markdown_links(text), [])

class TestSplitNodes(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "Link to [site1](http://one.com) and also [site2](http://two.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link to ", TextType.TEXT),
                TextNode("site1", TextType.LINK, "http://one.com"),
                TextNode(" and also ", TextType.TEXT),
                TextNode("site2", TextType.LINK, "http://two.com"),
            ],
            new_nodes
        )

    def test_no_markdown(self):
        node = TextNode("Just plain text.", TextType.TEXT)
        self.assertListEqual(split_nodes_image([node]), [node])
        self.assertListEqual(split_nodes_link([node]), [node])

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_combined(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and "
            "an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)
        self.assertListEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
