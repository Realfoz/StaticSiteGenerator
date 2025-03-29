import unittest
from htmlnode import ParentNode, LeafNode

def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )

def test_parent_node_with_no_props(self):
    child_node = LeafNode("b", "Bold text")
    parent_node = ParentNode("p", [child_node])
    self.assertEqual(parent_node.to_html(), "<p><b>Bold text</b></p>")

def test_parent_node_with_props(self):
    child_node = LeafNode("span", "Text")
    parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
    self.assertEqual(parent_node.to_html(), '<div class="container" id="main"><span>Text</span></div>')

def test_multiple_children(self):
    child1 = LeafNode("span", "First")
    child2 = LeafNode("span", "Second")
    parent_node = ParentNode("div", [child1, child2])
    self.assertEqual(parent_node.to_html(), "<div><span>First</span><span>Second</span></div>")

def test_leaf_with_no_tag(self):
    child1 = LeafNode(None, "Plain text")
    child2 = LeafNode("b", "Bold text")
    parent_node = ParentNode("p", [child1, child2])
    self.assertEqual(parent_node.to_html(), "<p>Plain text<b>Bold text</b></p>")

def test_value_error_with_no_tag(self):
    with self.assertRaises(ValueError):
        ParentNode(None, [LeafNode("span", "Text")]).to_html()

def test_value_error_with_no_children(self):
    with self.assertRaises(ValueError):
        ParentNode("div", None).to_html()