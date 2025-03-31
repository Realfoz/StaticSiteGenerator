import unittest
from node_types import TextNode, TextType
from split_delimiter import split_nodes_delimiter, markdown_to_blocks  

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_with_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_no_delimiter_found(self):
        node = TextNode("This is text with no delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is text with no delimiter")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    
    def test_non_text_node_unchanged(self):
        node = TextNode("This is already code", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
            ],
        )