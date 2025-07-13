from textnode import *
from htmlnode import *
from generate_site import *
import sys

if __name__ == '__main__':
    basepath = "/" if not sys.argv[1] else sys.argv[1]
    static_src = "./static/"
    dest_path = "./docs/"
    static_configuration(static_src, dest_path)
    generate_page_recursive("./content/", "./template.html", dest_path, basepath)