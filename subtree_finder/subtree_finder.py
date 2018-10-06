from collections import defaultdict


__all__ = ['subtree_finder', 'compute_pre_post_order_values']


def get_parent_child_mapping(child_parent_map):
    """
    Get list of children for each non-leaf node.

    Args:
        child_parent_map (dict, list, tuple): child:parent mapping for each node in the DAG.

    Returns:
        dict: parent:[child1, child2, etc.] mapping of children for each non-leaf node.

    Examples:
        >>>print get_parent_child_mapping({2:1, 3:1, 4:3})
        {1: [2, 3], 3: [4]}
        >>>print get_parent_child_mapping([(2,1), (3,1), (4,3)])
        {1: [2, 3], 3: [4]}
    """
    parent_children_mapping = defaultdict(list)
    if isinstance(child_parent_map, dict):
        child_parent_map = list(child_parent_map.iteritems())
    for child, parent in child_parent_map:
        parent_children_mapping[parent].append(child)
    return parent_children_mapping

def get_tree(parent_child_map, parent_id):
    """
    Recursive function which obtains a graph representation of DAG given parent:children mapping.

    Args:
        parent_child_map (dict): parent:[child1, child2, etc.] mapping of children for each non-leaf node.
        parent_id: the starting node in each recursive call of the function.

    Returns:
        dict: representation of DAG where each key:value is a node:subtree where each subtree is itself a dict.

    Examples:
        >>>print get_tree({1: [2, 3], 3: [4]})
        {
            1: 
                {
                    2: {}, 
                    3: {
                        4: {}
                    }
                }
        }
    """ 
    child_tree = {}
    for child_id in parent_child_map.get(parent_id, []):
        child_output = get_tree(parent_child_map, child_id)
        child_tree.update(child_output)
    return {parent_id: child_tree}

def compute_pre_post_order_values(
        tree,
        parent_id=None,
        parent_preorder=1,
):
    """
    Recursive function which computes pre and post order numbers for nodes given a dictionary represenation of a DAG (Directed Acyclic Graph).

    Args:
        tree (dict): representation of DAG where each key:value is a node:subtree where each subtree is itself a dict.
        parent_id: the starting node in each recursive call of the function.

    Returns:
        dict: where each key:value is node: {'preorder': int, 'postorder':int}

    Examples:
        >>>compute_pre_post_order_values({1: {2: {}, 3: {4: {}}}})
        {
            1: {'postorder': 8, 'preorder': 1},
            2: {'postorder': 3, 'preorder': 2},
            3: {'postorder': 7, 'preorder': 4},
            4: {'postorder': 6, 'preorder': 5}
        }
    """
    # if we don't get a parent_id, we infer it to be the top level node
    parent_id = parent_id or next(iter(tree))

    pre_post_parent = {
        parent_id: {
            "preorder": parent_preorder,
        }
    }

    child_postorder = None
    # sorted to make result deterministic
    children_ids = sorted(tree[parent_id].keys())
    for child_id in children_ids:
        # if child_postorder is set we know this is not the first child and can set preorder relative to previous child
        child_preorder = child_postorder + 1 if child_postorder else parent_preorder + 1

        pre_post_child = compute_pre_post_order_values(
            tree[parent_id],
            child_id, 
            child_preorder)
        pre_post_parent.update(pre_post_child)
        child_postorder = pre_post_child[child_id]["postorder"]
    # if children, parent post order is one more than last child post order; if leafnode, then postorder is one more than preorder
    pre_post_parent[parent_id]["postorder"] = pre_post_child[child_id]["postorder"] + 1 if children_ids else parent_preorder + 1

    return pre_post_parent

def subtree_finder(child_parent_map, starting_node):
    """
    Discovers reachable nodes in a DAG given child:parent information as a starting point.
        
        Args:
            child_parent_map (dict): child:parent mapping for each node in the DAG.

        Returns:
            list: of nodes that are reachable from the starting node, inclusive of starting node

        Examples:
            >>>subtree_finder({2:1, 3:1, 4:3}, 3)
            [3, 4]
    """
    parent_children_mapping = get_parent_child_mapping(child_parent_map)
    if starting_node  not in parent_children_mapping:
        return "Please enter valid starting node"
    dag = get_tree(parent_children_mapping, starting_node)
    pre_post_order_values = compute_pre_post_order_values(dag)

    return [
        node for node in pre_post_order_values if 
        pre_post_order_values[node]['postorder'] <= pre_post_order_values[starting_node]['postorder'] and
        pre_post_order_values[node]['preorder'] >= pre_post_order_values[starting_node]['preorder']
    ]
