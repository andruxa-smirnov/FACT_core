import unittest
from helperFunctions.compare_sets import intersection_of_list_of_sets, difference_of_sets, collapse_pair_of_sets, remove_duplicates_from_list_of_lists, index_of_other_list_including_item, safely_remove_pair_of_sets, make_pairs_of_sets


class TestHelperFunctionsCompareSets(unittest.TestCase):

    def test_intersect_list_of_sets(self):
        result = intersection_of_list_of_sets([])
        self.assertEqual(result, set(), 'result if no set is compared is not an empty set')
        a = set('abc')
        b = set('bcd')
        c = set('cde')
        result = intersection_of_list_of_sets([a, b, c])
        self.assertEqual(result, set('c'), 'result not correct')

    def test_difference_set_list_of_sets(self):
        base = set('abcde')
        a = set('bcd')
        b = set('ef')
        result = difference_of_sets(base, [a, b])
        self.assertEqual(result, set('a'), 'result not correct')

    def test_collapse_pair_of_sets(self):
        l1 = ({2, 4}, {4, 9})
        l2 = {2, 4, 9}
        self.assertEqual(collapse_pair_of_sets(l1), l2, 'pair collapsing doesn\'t work')

    def test_remove_duplicates_from_list_of_lists(self):
        l1 = [[2, 4], [5, 9], [2, 5], [6, 7], [1, 3, 12], [4, 2], [1, 12, 3], [2, 4], [2, 4], [2, 4]]
        l2 = [[2, 4], [5, 9], [2, 5], [6, 7], [1, 3, 12]]
        self.assertEqual(remove_duplicates_from_list_of_lists(l1), l2, 'result not correct')

    def test_item_in_other_list(self):
        other_list = [[2, 5], [6, 7], [1, 3, 12], [4, 2], [1, 7, 3]]
        item = 12
        self.assertGreater(index_of_other_list_including_item(other_list, item, 0), 0, 'item identification corrupt')
        self.assertLess(index_of_other_list_including_item(other_list, item, 2), 0, 'item identification corrupt')

    def test_safely_remove_pair_of_sets(self):
        test_list = [[2, 5], [6, 7], [1, 3, 12], [4, 2], [1, 7, 3]]
        safely_remove_pair_of_sets(test_list, ([2, 5], [6, 5]))
        self.assertNotIn([2, 5], test_list, 'Safe remove not working')

    def test_make_pairs_of_sets(self):
        test_list = [{2, 4}, {4, 9}, {1}, {3}]
        pairs = make_pairs_of_sets(test_list)
        self.assertEqual(len(pairs), 12, 'Not all pairs found - ordering is duplicated')
        self.assertIsInstance(pairs[0], tuple, 'pair is not a tuple')
        self.assertIn(({1}, {3}), pairs, 'Not all pairs found')
