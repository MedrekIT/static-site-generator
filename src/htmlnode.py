class HTMLNode:
    def __init__(self=None, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props:
            props_to_print = self.props.items()
            return f" {'" '.join(map(lambda prop: '="'.join(prop), props_to_print))}\""
        return ""
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("invalid HTML: value required")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("invalid HTML: tag required")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        for child in self.children:
            if type(child) == LeafNode and child.value == None:
                raise ValueError("invalid HTML: node child missing a value")
        return f"<{self.tag}{self.props_to_html()}>{''.join(map(lambda child: child.to_html(), self.children))}</{self.tag}>"