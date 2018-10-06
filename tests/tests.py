import unittest
from collections import defaultdict

from subtree_finder.subtree_finder import get_tree, get_parent_child_mapping, compute_pre_post_order_values, subtree_finder

class DAGNodeOrderTest(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.child_parent_mapping = {
			1: None,
			2: 1,
			3: 2,
			4: 2,
			5: 2,
			6: 3,
			10: 5,
			11: 5,
			12: 5,
			7: 6,
			8: 6,
			9: 6,
			13: 11,
			14: 11,
		}
		cls.parent_children_mapping = {
			None: [1],
			1: [2],
			2: [3, 4, 5],
			3: [6],
			5: [10, 11, 12],
			6: [7, 8, 9],
			11: [13, 14]
		}
		cls.dag = {
			1: {
				2: {
					3: {
						6: {
							7: {},
							8: {},
							9: {}
						},
					},
					4: {},
					5: {
						10: {},
						11: {
							13: {},
							14: {}
						},
						12: {}
					}
				}
			}
		}

	def test_get_parent_child_map(self):
		# arg as dict
		parent_children_map = get_parent_child_mapping(self.child_parent_mapping)
		self.assertDictEqual(parent_children_map, self.parent_children_mapping)

		# arg as list
		parent_children_map = get_parent_child_mapping(list(self.child_parent_mapping.iteritems()))
		self.assertDictEqual(parent_children_map, self.parent_children_mapping)

	def test_get_tree(self):
		dag = get_tree(self.parent_children_mapping, 1)
		self.assertDictEqual(dag, self.dag)

	def test_pre_post_order_values(self):
		pre_post_order_values = compute_pre_post_order_values(self.dag)
		self.assertEqual(
			pre_post_order_values,
			{
				1: {'postorder': 28, 'preorder': 1},
				2: {'postorder': 27, 'preorder': 2},
				3: {'postorder': 12, 'preorder': 3},
				4: {'postorder': 14, 'preorder': 13},
				5: {'postorder': 26, 'preorder': 15},
				6: {'postorder': 11, 'preorder': 4},
				7: {'postorder': 6, 'preorder': 5},
				8: {'postorder': 8, 'preorder': 7},
				9: {'postorder': 10, 'preorder': 9},
				10: {'postorder': 17, 'preorder': 16},
				11: {'postorder': 23, 'preorder': 18},
				12: {'postorder': 25, 'preorder': 24},
				13: {'postorder': 20, 'preorder': 19},
				14: {'postorder': 22, 'preorder': 21}
			 }
		)
	def test_get_children(self):
		reachable_nodes = subtree_finder(self.child_parent_mapping, 5)
		self.assertEqual(set(reachable_nodes), set([5, 10, 11, 13, 14, 12]))

