import re
from enum import Enum
from htmlnode import LeafNode, ParentNode

class TextType(Enum):
    NORMAL  = 'normal'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class BlockType(Enum):
    PARAGRAPH  = 'paragraph'
    HEAD = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED = 'unordered_list'
    ORDERED = 'ordered_list'

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
            if len(images) == 0:
                inner_nodes.append(TextNode(inner_text, TextType.NORMAL))
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
            if len(links) == 0:
                inner_nodes.append(TextNode(inner_text, TextType.NORMAL))
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
    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        [TextNode(text, TextType.NORMAL)], '**', TextType.BOLD)
                , '_', TextType.ITALIC)
            , '`', TextType.CODE)
        )
    )

def markdown_to_blocks(markdown):
    md_blocks = markdown.split("\n\n")
    md_no_whitespace = list(map(lambda block: block.strip(), md_blocks))
    md_clean = list(filter(lambda block: block != '', md_no_whitespace))
    return md_clean

def block_to_block_type(md_block):
    lines = md_block.split("\n")
    if re.match(r"(^#+ ).+", md_block): return BlockType.HEAD
    if len(lines) > 1 and re.match(r"(^```)", lines[0]) and re.match(r"```$", lines[-1]): return BlockType.CODE
    if re.match(r"(^>).+", md_block):
        for line in lines:
            if not re.match(r"(^>).+", line):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if re.match(r"(^- ).+", md_block):
        for line in lines:
            if not re.match(r"(^- ).+", line):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED
    if re.match(r"(^1. ).+", md_block):
        for i, line  in enumerate(lines, start=1):
            if not re.match(rf"(^{i}. ).+", line):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED
    return BlockType.PARAGRAPH

def text_to_children(markdown):
    nodes = text_to_textnodes(markdown)
    children = []

    for node in nodes:
        html_node = text_to_html(node)
        children.append(html_node)
    
    return children

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    children = []

    for block in md_blocks:
        html_node = block_to_html(block)
        children.append(html_node)
    
    return ParentNode("div", children)

def block_to_html(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html(block)
    if block_type == BlockType.HEAD:
        return heading_to_html(block)
    if block_type == BlockType.CODE:
        return code_to_html(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html(block)
    if block_type == BlockType.UNORDERED:
        return ulist_to_html(block)
    if block_type == BlockType.ORDERED:
        return olist_to_html(block)

def paragraph_to_html(block):
    paragraph = " ".join(block.split("\n"))
    children = text_to_children(paragraph)

    return ParentNode("p", children)

def heading_to_html(block):
    value = 0

    for char in block:
        if char == '#': value += 1
        else: break
    
    content = block[value + 1:]
    children = text_to_children(content)

    return ParentNode(f"h{value}", children)

def code_to_html(block):
    content = block[3:-3]
    text_node = TextNode(content, TextType.NORMAL)
    child = text_to_html(text_node)
    code = ParentNode("code", [child])

    return ParentNode("pre", [code])

def quote_to_html(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)

    return ParentNode("blockquote", children)

def ulist_to_html(block):
    items = block[2:].split("\n- ")
    html_items = []

    for item in items:
        children = text_to_children(item)
        html_items.append(ParentNode("li", children))
    
    return ParentNode("ul", html_items)

def olist_to_html(block):
    items = block.split("\n")
    html_items = []

    for item in items:
        new_text = item[3:]
        children = text_to_children(new_text)
        html_items.append(ParentNode("li", children))
    
    return ParentNode("ol", html_items)