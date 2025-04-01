from node_types import TextNode, TextType, BlockType
from htmlnode import HTMLNode,ParentNode,LeafNode, text_node_to_html_node
import re 


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []  # Initialize an empty list to store the resulting nodes

    if not isinstance(old_nodes, list):
        raise TypeError("old_nodes must be a list of TextNode objects")
    
    for node in old_nodes:  # Iterate over each node in the list
        if node.text_type == TextType.TEXT:  # Only split text-type nodes
            parts = node.text.split(delimiter)
            
            if len(parts) == 1:  # No delimiter found at all
                new_nodes.append(node)  # Keep the node unchanged

            elif len(parts) == 2:  # Only one delimiter found (opening without closing)
                raise ValueError(f"Mismatched or missing delimiters for '{delimiter}' in: {node.text}")
            
            else:              
                # Create new nodes for before, middle, and after parts
                before_node = TextNode(parts[0], TextType.TEXT)  # Before part
                middle_node = TextNode(parts[1], text_type)  # Middle part, converted to provided text_type
                after_node = TextNode(parts[2], TextType.TEXT)  # After part
                
                # Add them to the result list
                new_nodes.extend([before_node, middle_node, after_node])
        else:
            new_nodes.append(node) # Add the non-text node directly to the list
    return new_nodes  # Ensure the fully constructed list is returned


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:  # Iterate over each node in the list
        if node.text_type != TextType.IMAGE: 
            image_tuples = extract_markdown_images(node.text)
            if not image_tuples:  # if no images found, add the node as is
                result.append(node)
            else:
                current_text = node.text  # Initialize current_text
                for alt_text, url in image_tuples:
                    # Split the current text at the image markdown
                    image_markdown = f"![{alt_text}]({url})"
                    parts = current_text.split(image_markdown, 1)
                    
                    # Add a text node for the part before the image (if not empty)
                    if parts[0]:
                        result.append(TextNode(parts[0], TextType.TEXT))
                    
                    # Add the image node
                    result.append(TextNode(alt_text, TextType.IMAGE, url))
                    
                    # The remaining text becomes the current text for the next iteration
                    current_text = parts[1] if len(parts) > 1 else ""
                
                # Add any remaining text after all images are processed
                if current_text:
                    result.append(TextNode(current_text, TextType.TEXT))
        else:
            result.append(node)
    return result  # Return result after processing all nodes




def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:  # Iterate over each node in the list
        if node.text_type != TextType.LINK: 
            links = extract_markdown_links(node.text)
            if not links:  # if no link found, add the node as is
                result.append(node)
            else:
                current_text = node.text  # Initialize current_text
                for text, url in links:
                    # Split the current text at the link markdown
                    link_markdown = f"[{text}]({url})"
                    parts = current_text.split(link_markdown, 1)
                    
                    # Add a text node for the part before the link (if not empty)
                    if parts[0]:
                        result.append(TextNode(parts[0], TextType.TEXT))
                    
                    # Add the link node
                    result.append(TextNode(text, TextType.LINK, url))
                    
                    # The remaining text becomes the current text for the next iteration
                    current_text = parts[1] if len(parts) > 1 else ""
                
                # Add any remaining text after all link are processed
                if current_text:
                    result.append(TextNode(current_text, TextType.TEXT))
        else:
            result.append(node)
    return result  # Return result after processing all nodes



def markdown_to_blocks(markdown):
    final_list = []
    # Strip leading/trailing whitespace or newlines from the entire input
    split_lines = markdown.strip().split("\n\n")
    for line in split_lines:
        if line.strip():  # Only process non-empty blocks
            # Clean up each block while preserving internal structure
            stripped_block = "\n".join(subline.strip() for subline in line.split("\n"))
            final_list.append(stripped_block)
    return final_list




def block_to_block_type(block):
    # Check for heading
    if block.startswith("#"):
        parts = block.split(" ", 1)
        if len(parts) > 1 and 1 <= len(parts[0]) <= 6 and all(char == '#' for char in parts[0]):
            return BlockType.heading
    
    # Check for code block
    
    stripped_lines = [line.strip() for line in block.split('\n')]
    if len(stripped_lines) >= 2 and stripped_lines[0] == "```" and stripped_lines[-1] == "```":
        return BlockType.code
    
    # Split into lines for multi-line checks
    lines = block.split("\n")
    
    # Check for quote block
    if all(line.startswith(">") for line in lines):
        return BlockType.quote
    
    # Check for unordered list
    if all(line.startswith("- ") for line in lines):
        return BlockType.unordered_list
    
    # Check for ordered list using function below
    if lines and is_ordered_list(block):
        return BlockType.ordered_list
    
    return BlockType.paragraph
        

def is_ordered_list(block):
    lines = block.split("\n")
    for i, line in enumerate(lines):
        expected_start = f"{i+1}. "
        if not line.startswith(expected_start):
            return False
    return True        


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)  # Split the markdown into blocks
    parent_node = ParentNode("div", [], None)   # Create a parent "div" node for all content
    
    for block in blocks:
        block_type = block_to_block_type(block)  # Determine type of block
        text = ""  # Initialize the text variable
        
        if block_type == BlockType.paragraph:
            # Replace newlines with spaces in paragraph text
            text = " ".join([line.strip() for line in block.split("\n") if line.strip()])
            html_node = ParentNode("p", text_to_children(text))
            parent_node.children.append(html_node)
        
        elif block_type == BlockType.heading:
            level = block.count("#", 0, block.index(" "))  # Number of "#" defines the level
            text = block[level + 1:].strip()  # Extract the text without the heading markers
            html_node = ParentNode(f"h{level}", text_to_children(text))
            parent_node.children.append(html_node)
        
        elif block_type == BlockType.code:
            # Create code block node
            code_content = clean_code_block(block)
            code_node = ParentNode("code",[TextNode(code_content, TextType.TEXT)])
            pre_node = ParentNode("pre", [code_node])
            parent_node.children.append(pre_node)
        
        elif block_type == BlockType.quote:
            text = block[1:].strip()  # Remove the ">" marker and surrounding whitespace
            html_node = ParentNode("blockquote", text_to_children(text))
            parent_node.children.append(html_node)
        
        elif block_type == BlockType.ordered_list:
            lines = block.splitlines()  # Split ordered list into individual items
            list_items = []
            for line in lines:
                item_text = line.lstrip("0123456789. ").strip()  # Remove "1. " or similar
                list_items.append(ParentNode("li", text_to_children(item_text)))
            html_node = ParentNode("ol", list_items)
            parent_node.children.append(html_node)
        
        elif block_type == BlockType.unordered_list:
            lines = block.splitlines()  # Split unordered list into individual items
            list_items = []
            for line in lines:
                item_text = line.lstrip("- ").strip()  # Remove "- " or similar
                list_items.append(ParentNode("li", text_to_children(item_text)))
            html_node = ParentNode("ul", list_items)
            parent_node.children.append(html_node)
    return parent_node


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

def clean_code_block(block):
    # Strip leading/trailing whitespace from each line
    lines = [line.rstrip() for line in block.split('\n')]
    
    # Find the first and last line with backticks
    start_idx = -1
    end_idx = -1
    
    for i, line in enumerate(lines):
        if line.strip() == "```":
            if start_idx == -1:
                start_idx = i
            else:
                end_idx = i
                break
    
    # If we found both start and end markers
    if start_idx != -1 and end_idx != -1:
        # Extract lines between the backticks (excluding the backticks themselves)
        code_lines = lines[start_idx + 1:end_idx]
        return "\n".join(code_lines)
    
    # Fallback - this shouldn't happen if block_to_block_type correctly identifies code blocks
    return block

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes
