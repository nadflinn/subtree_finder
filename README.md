# subtree_finder

This is a utility that finds a subtree in a DAG (directed acyclic graph) given a starting node and inclusive of that starting node.  

For example given a tree like the following:

```
        Parent
        /     \
    Child1  Child2
     / \      /
   GC1 GC2  GC3
```

If we want to know which nodes are reachable from `Child1`, `subtree_finder` can tell us.

The input should be a dictionary with key:value pairs representing child:parent or a list or tuple with (child, parent) items: 

```
{
	'Child1': 'Parent', 
	'Child2': 'Parent', 
	'GC1': 'Child1',
	'GC2': 'Child1',
	'GC3': 'Child2',
}

[('Child1', 'Parent'),
 ('Child2', 'Parent'),
 ('GC1', 'Child1'),
 ('GC2', 'Child1'),
 ('GC3', 'Child2')]
```

Example:
```
subtree_finder({'Child1': 'Parent', 'Child2': 'Parent', 'GC1': 'Child1', 'GC2': 'Child1', 'GC3': 'Child2'}, 'Child1')
['GC1', 'Child1', 'GC2']
```

Also exposed in this library is:

```
compute_pre_post_order_values
```

`compute_pre_post_order_values` computes the preorder and postorder values as calculated during a run of depth first search on a DAG. The basic idea for pre-order and post-order values is that each node is assigned a pre-order value when first reached.  A post order number is assigned after all nodes reachable from that node have been explored.  So a leaf node, for example, will have consecutive pre-order and post-order numbers. It's parent node will not.

These pre and post order numbers also happen to represent nested sets which are useful in determining which nodes are the children of (or reachable from) any given node.  Specifically given node A, any nodes whose pre-order and post-order range fits wholly within the pre-order, post-order range of node A will be children of node A.

For example, in the table below, B and C are children of A, while D is not.

```
    Pre  | Post
    ---    ---
A    1   |  6
B    2   |  5
C    3   |  4
D    7   |  8
```

Given a representation of a DAG `compute_pre_post_order_values` finds the pre and post order values for each node.  This is used in `subtree_finder`.

Example:
```
>>>compute_pre_post_order_values({1: {2: {}, 3: {4: {}}}})
{
    1: {'postorder': 8, 'preorder': 1},
    2: {'postorder': 3, 'preorder': 2},
    3: {'postorder': 7, 'preorder': 4},
    4: {'postorder': 6, 'preorder': 5}
}
```

### Installation

```
python setup.py install
```

### Run Tests

```
python setup.py test
```

