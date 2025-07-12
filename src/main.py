from textnode import *
from htmlnode import *
from generate_site import *

if __name__ == '__main__':
    generate_page("./content/index.md", "./template.html", "./public/index.html")