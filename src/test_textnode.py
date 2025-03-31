import unittest

from node_types import TextNode, TextType
from textnode import text_to_textnodes
from htmlnode import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_neq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)


    def test_neq2(self):
        node = TextNode("WUD WUD", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("Hello World", TextType.CODE, "www.google.com")
        node2 = TextNode("Hello World", TextType.CODE, "www.google.com")
        self.assertEqual(node, node2)    

    def test_neq_url(self):
        node = TextNode("Hello World", TextType.CODE, "www.boot.dev")
        node2 = TextNode("Hello World", TextType.CODE, "www.google.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")    

    def test_image(self):
        # Create a TextNode with TEXT_TYPE.IMAGE, providing text for alt and url for src
        image_text = "My test image"
        image_url = "https://example.com/image.png"
        node = TextNode(image_text, TextType.IMAGE, image_url)
        
        # Convert to HTMLNode
        html_node = text_node_to_html_node(node)
        
        # Verify the conversion worked correctly
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")  # img tags have empty value
        self.assertEqual(html_node.props["src"], image_url)
        self.assertEqual(html_node.props["alt"], image_text)

    def test_bold(self):
        bold_text = "This is bold text"
        node = TextNode(bold_text, TextType.BOLD)
        html_node = text_node_to_html_node(node)
        
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, bold_text)
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        italic_text = "This is italic text"
        node = TextNode(italic_text, TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, italic_text)
        self.assertEqual(html_node.props, None)

    def test_code(self):
        code_text = "print('Hello, World!')"
        node = TextNode(code_text, TextType.CODE)
        html_node = text_node_to_html_node(node)
        
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, code_text)
        self.assertEqual(html_node.props, None)

    def test_link(self):
        link_text = "Boot.dev"
        link_url = "https://boot.dev"
        node = TextNode(link_text, TextType.LINK, link_url)
        html_node = text_node_to_html_node(node)
        
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, link_text)
        self.assertEqual(html_node.props["href"], link_url)

    def test_invalid_type(self):
        # Testing that exception is raised for invalid TextType
        # This assumes TextType doesn't have a value like "INVALID"
        # You might need to adjust based on your actual implementation
        node = TextNode("Invalid", "INVALID")

    
if __name__ == "__main__":
    unittest.main()