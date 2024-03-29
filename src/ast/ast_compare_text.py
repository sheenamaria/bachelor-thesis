import re

from src.ast.ast_utils import get_name_from_uid, traverse_ast, is_class


def generate_change_text_for_file(file_name, compare_tree):
    change_model = compare_tree
    root = change_model
    generated_text = ""

    def generate(node, parent, level):
        nonlocal generated_text
        text = generate_change_text(node, parent, level)
        generated_text += text

    traverse_ast(root, generate)
    if generated_text:
        if root["change"]["type"] == "add":
            return f"The file {file_name} has been added, the following additions have been made: {generated_text}"
        elif root["change"]["type"] == "delete":
            return f"The file {file_name} has been deleted, the following deletions have been made: {generated_text}"
        else:
            return f"In the file {file_name}, the following changes have been made: {generated_text}"
    else:
        if generated_text == "":
            pass
        return generated_text


def generate_change_text(node, parent, level):
    if is_class(node):
        return generate_file_text(node, parent, level)
    return ""


def format_methods(method_list, action):
    if len(method_list) == 1:
        return f"the method {method_list[0]} was {action}"
    elif len(method_list) == 2:
        return f"the methods {method_list[0]} and {method_list[1]} were {action}"
    elif len(method_list) > 2:
        first_methods = ", ".join(method_list[:-1])
        last_method = method_list[-1]
        return f"the methods {first_methods}, and {last_method} were {action}"


def generate_file_text(node, parent, level):
    class_name = get_name_from_uid(node["uid"])
    added_methods = []
    deleted_methods = []
    modified_methods = []

    for i, child in enumerate(node["children"]):
        method_name = get_name_from_uid(node["children"][i]["uid"])
        change_type = node["children"][i]["change"]["type"]

        if change_type == "add":
            added_methods.append(method_name)
        elif change_type == "delete":
            deleted_methods.append(method_name)
        elif change_type == "modify":
            modified_methods.append(method_name)

    added_text = format_methods(added_methods, "added")
    deleted_text = format_methods(deleted_methods, "deleted")
    modified_text = format_methods(modified_methods, "modified")

    text_parts = []
    if added_text:
        text_parts.append(added_text)
    if deleted_text:
        text_parts.append(deleted_text)
    if modified_text:
        text_parts.append(modified_text)
    if text_parts:
        text = f"In the class {class_name}, {' and '.join(text_parts)}."
    else:
        text = ""
    return text


def change_text_camel_case_splitter(change_text):
    return re.sub(r"([a-z])([A-Z])", r"\1 \2", change_text)
