import unittest
import time
from dz_33 import bubble_sort, quick_sort, radix_sort

class TestSorting(unittest.TestCase):

    def setUp(self):
        self.unsorted_list = [64, 34, 25, 12, 22, 11, 90]
        self.sorted_list = [11, 12, 22, 25, 34, 64, 90]
        self.empty_list = []
        self.single_element = [5]

    def test_bubble_sort_correct(self):
        arr = self.unsorted_list.copy()
        bubble_sort(arr)
        self.assertEqual(arr, self.sorted_list)

    def test_quick_sort_correct(self):
        arr = self.unsorted_list.copy()
        result = quick_sort(arr)
        self.assertEqual(result, self.sorted_list)

    def test_radix_sort_correct(self):
        arr = self.unsorted_list.copy()
        radix_sort(arr)
        self.assertEqual(arr, self.sorted_list)

if __name__ == '__main__':
    unittest.main()

