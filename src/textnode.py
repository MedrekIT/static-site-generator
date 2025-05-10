import re
from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    NORMAL  = 'normal'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        if self.url:
            return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        return f"TextNode({self.text}, {self.text_type.value})"

def text_to_html(text_node: TextNode):
        match text_node.text_type:
            case TextType.NORMAL:
                return LeafNode(None, text_node.text)
            case TextType.BOLD:
                return LeafNode("b", text_node.text)
            case TextType.ITALIC:
                return LeafNode("i", text_node.text)
            case TextType.CODE:
                return LeafNode("code", text_node.text)
            case TextType.LINK:
                return LeafNode("a", text_node.text, {"href": text_node.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            case _:
                raise Exception(f"invalid text type: {text_node.text_type}")
            
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            inner_nodes = []
            inner_text = node.text.split(delimiter)
            if len(inner_text) % 2 == 0:
                raise ValueError("invalid markdown file format")
            for i in range(len(inner_text)):
                if inner_text[i] == "":
                    continue
                if i % 2 == 0:
                    inner_nodes.append(TextNode(inner_text[i], node.text_type))
                else:
                    inner_nodes.append(TextNode(inner_text[i], text_type))
            new_nodes.extend(inner_nodes)
            continue
        new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            inner_nodes = []
            inner_text = node.text
            images = extract_markdown_images(node.text)
            for i in range(len(images)):
                inner_text = inner_text.split(f"![{images[i][0]}]({images[i][1]})")
                if inner_text[0] == "":
                    inner_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
                    inner_text = inner_text[1]
                    continue
                if i == len(images)-1 and inner_text[1]:
                    inner_nodes.append(TextNode(inner_text[0], TextType.NORMAL))
                    inner_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
                    inner_nodes.append(TextNode(inner_text[1], TextType.NORMAL))
                else:
                    inner_nodes.append(TextNode(inner_text[0], TextType.NORMAL))
                    inner_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
                    if inner_text[1]:
                        inner_text = inner_text[1]
            new_nodes.extend(inner_nodes)
            continue
        new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            inner_nodes = []
            inner_text = node.text
            links = extract_markdown_links(node.text)
            for i in range(len(links)):
                inner_text = inner_text.split(f"[{links[i][0]}]({links[i][1]})")
                if inner_text[0] == "":
                    inner_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
                    inner_text = inner_text[1]
                    continue
                if i == len(links)-1 and inner_text[1]:
                    inner_nodes.append(TextNode(inner_text[0], TextType.NORMAL))
                    inner_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
                    inner_nodes.append(TextNode(inner_text[1], TextType.NORMAL))
                else:
                    inner_nodes.append(TextNode(inner_text[0], TextType.NORMAL))
                    inner_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
                    if inner_text[1]:
                        inner_text = inner_text[1]
            new_nodes.extend(inner_nodes)
            continue
        new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    return split_nodes_delimiter(
        split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_image(
                    split_nodes_link(text)
                ), '`', TextType.CODE
            ), '_', TextType.ITALIC
        ), '**', TextType.BOLD
    )