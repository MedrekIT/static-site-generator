from textnode import *
from htmlnode import *
from generate_site import *

if __name__ == '__main__':
    static_configuration()
    generate_page_recursive("./content", "./template.html", "./public")