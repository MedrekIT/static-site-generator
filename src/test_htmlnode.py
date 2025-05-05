import unittest

from htmlnode import *


class TestHMTMLNode(unittest.TestCase):
    def test_props_empty(self):
        node = HTMLNode("p", "some_paragraph")
        node2 = HTMLNode("p", "some_paragraph", None, None)
        node3 = HTMLNode("p", "some_paragraph", props=None)
        self.assertEqual(node.props_to_html(), "")
        self.assertEqual(node2.props_to_html(), "")
        self.assertEqual(node3.props_to_html(), "")
    
    def test_props_one(self):
        node = HTMLNode("p", "some_paragraph", props={"href": "https://www.boot.dev"})
        node2 = HTMLNode("p", "some_paragraph", props={"href": "https://www.google.com"})
        node3 = HTMLNode("p", "some_paragraph", None, {"href": "https://www.boot.dev"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.boot.dev\"")
        self.assertEqual(node2.props_to_html(), " href=\"https://www.google.com\"")
        self.assertEqual(node3.props_to_html(), " href=\"https://www.boot.dev\"")

    def test_props_many(self):
        node = HTMLNode("p", "some_paragraph", props={"href": "https://www.boot.dev", "target": "_blank"})
        node2 = HTMLNode("p", "some_paragraph", [node], {"href": "https://www.boot.dev", "target": "_blank"})
        node3 = HTMLNode("p", "some_paragraph", None, {"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.boot.dev\" target=\"_blank\"")
        self.assertEqual(node2.props_to_html(), " href=\"https://www.boot.dev\" target=\"_blank\"")
        self.assertEqual(node3.props_to_html(), " href=\"https://www.boot.dev\" target=\"_blank\"")
    
    def test_values(self):
        node = HTMLNode("p", "some_paragraph")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "some_paragraph")
    
    def test_repr(self):
        node = HTMLNode("p", "some_paragraph", None, props={"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(node.__repr__(), "HTMLNode(p, some_paragraph, children: None, {'href': 'https://www.boot.dev', 'target': '_blank'})")
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click here", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click here</a>")
    
    def test_to_html_without_any_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_with_a_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_many_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("p", "child2")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><p>child2</p></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()