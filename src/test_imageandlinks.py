import unittest
from split_delimiter import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from node_types import TextNode,TextType


class TestMarkdownExtractors(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("Here is a link to [Boot.dev](https://www.boot.dev) and one to [Google](https://www.google.com)")
        self.assertListEqual(
            [("Boot.dev", "https://www.boot.dev"), ("Google", "https://www.google.com")],
            matches
        )

    def test_empty_text_link(self):
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)

    def test_empty_text_image(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)
        
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
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_single_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                
            ],
            new_nodes,
        )
    def test_split_single_link(self):
        node = TextNode(
            "Visit [my website](https://mysite.com) for more information.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])  # Changed to split_nodes_link
        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("my website", TextType.LINK, "https://mysite.com"),
                TextNode(" for more information.", TextType.TEXT)
            ],  # Added comma here
            new_nodes,
        )

    def test_image_and_link(self):
        # Start with text containing both an image and a link
        node = TextNode(
            "Here's an ![image](https://example.com/image.jpg) and a [link](https://example.com)",
            TextType.TEXT,
        )
        
        # First split by images
        nodes_after_images = split_nodes_image([node])
        
        # Then split the resulting nodes by links
        final_nodes = split_nodes_link(nodes_after_images)
        
        # Assert the final result has the expected nodes
        self.assertListEqual(
            [
                TextNode("Here's an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            final_nodes,
        )

            