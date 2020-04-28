#! /usr/bin/env python3

import unittest

from args import *

class DummyTest(unittest.TestCase):
    def test_case(self):
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
