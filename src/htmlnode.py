


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
        if not self.value:
            raise ValueError("must have a value") 

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
            raise ValueError("must have a tag")
        if not self.children:
            raise ValueError("must have a child")

        for child in self.children:
