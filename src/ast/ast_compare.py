from src.ast.ast_utils import get_parent_uid, create_ast_map


def compare_ast(before, after):
    changes = []

    left = create_ast_map(before)
    right = create_ast_map(after)

    for key, left_node in left.items():
        if key in right:
            right_node = right[key]
            left_node["children"] = []
            right_node["children"] = []
            change_type = (
                "modify"
                if (
                    left_node.get("fingerprint", None)
                    != right_node.get("fingerprint", None)
                )
                or (
                    left_node.get("composite_fingerprint", None)
                    != right_node.get("composite_fingerprint", None)
                )
                else "none"
            )
            change = {
                "uid": key,
                "type": left_node["type"],
                "change": {
                    "type": change_type,
                    "before": left_node,
                    "after": right_node,
                },
                "children": [],
            }
            changes.append(change)
    for change in changes:
        del left[change["uid"]]
        del right[change["uid"]]

    for key, left_node in left.items():
        if key not in right:
            change = {
                "uid": key,
                "type": left_node["type"],
                "change": {"type": "delete", "before": left_node, "after": None,},
                "children": [],
            }
            changes.append(change)
    for key, right_node in right.items():
        if key not in left:
            change = {
                "uid": key,
                "type": right_node["type"],
                "change": {"type": "add", "before": None, "after": right_node,},
                "children": [],
            }
            changes.append(change)

    for change in changes:
        if change.get("before") and change.get("after"):
            if change["type"] == "compilation-unit":
                if change["before"]["filename"] != change["after"]["filename"]:
                    change["rename"] = {
                        "before": change["before"]["filename"],
                        "after": change["after"]["filename"],
                    }
                if change["before"]["package"] != change["after"]["package"]:
                    change["move"] = {
                        "before": change["before"]["package"],
                        "after": change["after"]["package"],
                    }
            elif change["type"] == "class":
                if change["before"]["identifier"] != change["after"]["identifier"]:
                    change["rename"] = {
                        "before": change["before"]["identifier"],
                        "after": change["after"]["identifier"],
                    }

    return changes


def build_change_tree(changes):
    lookup = {}
    root = None
    for change in changes:
        lookup[change["uid"]] = change
    for i, change in enumerate(changes):
        pid = get_parent_uid(change["uid"])
        parent = lookup.get(pid)
        if parent is not None:
            parent["children"].append(change)
        else:
            if root is not None:
                pass
                raise Exception
            root = change
    return root
