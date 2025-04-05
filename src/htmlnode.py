from node_types import TextNode, TextType




class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):      
        raise NotImplementedError
    

    def props_to_html(self):
        if not self.props:
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"
    


class LeafNode(HTMLNode):
    
    def __init__(self, tag, value, props=None):
            # Ensure props is a dictionary or None
            if props is not None and not isinstance(props, dict):
              raise TypeError("props must be a dictionary")
            # Pass arguments to parent constructor explicitly
            super().__init__(tag=tag, value=value, children=None, props=props)

        

    def to_html(self):    
        if self.value is None:
            self.value = ""  # Set empty string instead of raising an error
        
        if self.tag is None:
            return self.value
        
        # Start building the opening tag
        html = f"<{self.tag}" 

        # Add props (attributes) if they exist
        if self.props:
            for prop, val in self.props.items():   
                html += f' {prop}="{val}"'

        # Close the opening tag, add value, and the closing tag
        html += f">{self.value}</{self.tag}>"
        
        return html

        

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
         super().__init__(tag=tag, value=None, children=children, props=props)


    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node missing tag")
               
        html = f"<{self.tag}"
    
        if self.props:
            for prop, val in self.props.items():   
                html += f' {prop}="{val}"'
    
        html += ">"
    
        children_html = ""   
        for child in self.children:
            children_html += child.to_html()
    
        html += children_html
        html += f"</{self.tag}>"
    
        return html
    

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
        
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)

    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", " ", {
        "src": text_node.url,  
        "alt": text_node.text
         })

    else:
        # Raise an exception for unknown TextType
        raise Exception(f"Invalid TextType: {text_node.text_type}")
    





    