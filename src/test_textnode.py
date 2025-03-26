import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()