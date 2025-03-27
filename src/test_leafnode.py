import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_href(self):
        node = LeafNode("a", "Hello, world!", {"href": "www.google.com"})
        self.assertEqual(node.to_html(), '<a href="www.google.com">Hello, world!</a>')
        
    
    def test_leaf_to_html_head(self):
        node = LeafNode("head", "BIG TITLE!")
        self.assertEqual(node.to_html(), "<head>BIG TITLE!</head>")
    
    def test_leaf_to_html_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text.")
        self.assertEqual(node.to_html(), "Just text.")

    def test_leaf_to_html_empty_props(self):
        node = LeafNode("p", "No props here!", {})
        self.assertEqual(node.to_html(), "<p>No props here!</p>")