import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html_with_props(self):
        # Test that props are converted correctly
        node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com" target="_blank"')
    
    def test_props_to_html_with_no_props(self):
        # Test with no props (should return empty string)
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_with_single_prop(self):
        # Test with a single property
        node = HTMLNode(props={"class": "header"})
        self.assertEqual(node.props_to_html(), ' class="header"')
    
    def test_initialization(self):
        # Test that all parameters are correctly assigned
        node = HTMLNode("p", "Hello, world!", [], {"class": "text"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, world!")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "text"})

if __name__ == "__main__":
    unittest.main()
