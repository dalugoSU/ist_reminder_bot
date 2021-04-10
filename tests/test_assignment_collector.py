import os
import sys
import unittest
import time

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from collector.collection import AssignmentCollector


class TestAssignmentCollector(unittest.TestCase):

    def setUp(self) -> None:
        self.collector = AssignmentCollector()


    def test_get_class_assignments(self):
        result = self.collector.get_class_assignments()
        self.assertEqual(len(result), 57)

    def test_get_date(self) -> None:
        today, tomorrow = self.collector.get_date()
        self.assertTrue(today, True)
        self.assertTrue(tomorrow, True)


if __name__ == "__main__":
    unittest.main()
