import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

        node9 = TextNode("This is a text node", TextType.ITALIC, 'https://www.boot.dev/')
        node10 = TextNode("This is a text node", TextType.ITALIC, 'https://www.boot.dev/')
        self.assertEqual(node9, node10)
    
    def test_uneq(self):
        node3 = TextNode("This is a node", TextType.NORMAL, None)
        node4 = TextNode("This is a text node", TextType.NORMAL)
        self.assertNotEqual(node3, node4)

        node5 = TextNode("This is a text node", TextType.ITALIC)
        node6 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node5, node6)

        node7 = TextNode("This is a node", TextType.ITALIC)
        node8 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node7, node8)

        node11 = TextNode("This is a text node", TextType.ITALIC, 'https://www.boot.dev/')
        node12 = TextNode("This is a text node", TextType.ITALIC, None)
        self.assertNotEqual(node11, node12)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_to_html(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_to_html(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        self.assertEqual(html_node.to_html(), "<code>This is a code node</code>")
    
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        html_node = text_to_html(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props_to_html(), " href=\"https://www.boot.dev\"")
        self.assertEqual(html_node.to_html(), "<a href=\"https://www.boot.dev\">This is a link node</a>")
    
    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_to_html(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props_to_html(), " src=\"https://www.boot.dev\" alt=\"This is an image node\"")
        self.assertEqual(html_node.to_html(), "<img src=\"https://www.boot.dev\" alt=\"This is an image node\"></img>")


if __name__ == "__main__":
    unittest.main()