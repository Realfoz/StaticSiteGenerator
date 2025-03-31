
from split_delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link
from node_types import TextNode, TextType


def text_to_textnodes(text):
    
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Handle special markdown elements first
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    # Then handle the delimiter-based formatting
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    return nodes