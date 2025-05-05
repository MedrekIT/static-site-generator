from textnode import *
from htmlnode import *

if __name__ == '__main__':
    new_node =  TextNode('This is some anchor text', TextType.LINK, 'https://www.boot.dev')
    print(new_node)

    new_html = HTMLNode("p", "first_paragraph", None, {"href": "https://www.boot.dev", "target": "_blank"})
    print(new_html, new_html.props_to_html())