from textnode import TextNode, TextType

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