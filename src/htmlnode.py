


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
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag, value, props)
        
    def to_html(self):
        if not self.value:
            raise ValueError("must have a value") # removes none value inputs 
        
        html = f"<{self.tag}" # adds the initial tag if it has one with the <

        if self.props:
            for prop, val in self.props.items():    # iterates over each prop to add each tuple to the html string with proper formating
                html += f' {prop}="{val}"'

        html += f">{self.value}</{self.tag}>" # finalizes the string with final values and tags
    
        return html
        
        