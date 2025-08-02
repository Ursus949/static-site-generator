import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        segments = node.text.split(delimiter)

        if len(segments) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")

        # Even indices: plain text, Odd indices: wrapped in delimiter
        for i, segment in enumerate(segments):
            if segment == "":
                continue  # ignore empty segments

            if i % 2 == 0:
                new_nodes.append(TextNode(segment, TextType.TEXT))
            else:
                new_nodes.append(TextNode(segment, text_type))

    return new_nodes

def extract_markdown_images(text):
    """
    Extracts all markdown images from the text.

    Returns:
        List[Tuple[str, str]]: List of (alt_text, url) tuples
    """
    return re.findall(r"!\[([^\]]+)\]\(([^)]+)\)", text)

def extract_markdown_links(text):
    """
    Extracts all markdown links (excluding images) from the text.

    Returns:
        List[Tuple[str, str]]: List of (anchor_text, url) tuples
    """
    return re.findall(r"(?<!\!)\[([^\]]+)\]\(([^)]+)\)", text)

