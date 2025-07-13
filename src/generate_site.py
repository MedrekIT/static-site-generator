from os import listdir, path, mkdir
from shutil import rmtree, copy
from textnode import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line.lstrip("#").strip()

    raise Exception("There is no title in the file")

def clear_path(dest_path):
    if path.exists(dest_path):
        rmtree(dest_path)
    mkdir(dest_path)

def copy_static_content(static_path, dest_path, inner_path=""):
    for element in listdir(static_path):
        element_path = f"{static_path}{element}"
        if not path.isfile(element_path):
            if not path.exists(f"{dest_path}{inner_path}{element}"):
                mkdir(f"{dest_path}{inner_path}{element}")
            new_path = f"{inner_path}{element}/"
            copy_static_content(f"{element_path}/", dest_path, new_path)
        else:
            print(element_path, f"{dest_path}{inner_path}")
            copy(element_path, f"{dest_path}{inner_path}")

def static_configuration(static_src, dest_path):
    clear_path(dest_path)
    copy_static_content(static_src, dest_path)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for element in listdir(dir_path_content):
        element_path = f"{dir_path_content}{element}"
        if not path.isfile(element_path):
            print(element_path)
            if not path.exists(f"{dest_dir_path}{element}"):
                mkdir(f"{dest_dir_path}{element}")
            generate_page_recursive(f"{element_path}/", template_path, f"{dest_dir_path}{element}/", basepath)
        else:
            element_type = element.split(".")
            if element_type[1] == "md":
                generate_page(element_path, template_path, f"{dest_dir_path}{element_type[0]}.html", basepath)
            else: raise Exception(f"Invalid file type in {dir_path_content} directory")

def generate_page(from_path, template_path, dest_path, basepath):
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
    page_with_content = titled_contents.replace("{{ Content }}", html_contents)
    href_changed = page_with_content.replace("href=\"/", f"href=\"{basepath}")
    page_updated = href_changed.replace("src=\"/", f"src=\"{basepath}")

    with open(dest_path, "w") as f:
        f.write(page_updated)
    f.close()