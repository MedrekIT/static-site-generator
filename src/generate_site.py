from os import listdir, path, mkdir
from shutil import rmtree, copy
from textnode import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line.lstrip("#").strip()

    raise Exception("There is no title in the file")

def clear_path():
    if path.exists(f"./public"):
        rmtree("./public")
    mkdir("./public")

def copy_static_content(static_path, inner_path=""):
    for element in listdir(static_path):
        element_path = f"{static_path}/{element}"
        if not path.isfile(element_path):
            if not path.exists(f"./public/{inner_path}{element}"):
                mkdir(f"./public/{inner_path}{element}")
            new_path = f"{inner_path}/{element}/"
            copy_static_content(element_path, new_path)
        else: copy(element_path, f"./public/{inner_path}")

def static_configuration():
    clear_path()
    copy_static_content("./static")

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    for element in listdir(dir_path_content):
        element_path = f"{dir_path_content}/{element}"
        if not path.isfile(element_path):
            print(element_path)
            if not path.exists(f"{dest_dir_path}/{element}"):
                mkdir(f"{dest_dir_path}/{element}")
            generate_page_recursive(f"{dir_path_content}/{element}", template_path, f"{dest_dir_path}/{element}")
        else:
            element_type = element.split(".")
            if element_type[1] == "md":
                generate_page(f"{dir_path_content}/{element}", template_path, f"{dest_dir_path}/{element_type[0]}.html")
            else: raise Exception(f"Invalid file type in {dir_path_content} directory")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        md_contents = f.read()
    f.close()

    with open(template_path) as f:
        template_contents = f.read()
    f.close()

    html_node = markdown_to_html_node(md_contents)
    html_contents = html_node.to_html()

    page_title = extract_title(md_contents)

    titled_contents = template_contents.replace("{{ Title }}", page_title)
    page_contents = titled_contents.replace("{{ Content }}", html_contents)

    with open(dest_path, "w") as f:
        f.write(page_contents)
    f.close()