import unittest

import logging

from dotgit.args import Arguments

class ArgumentsTests(unittest.TestCase):
    def test_verbose(self):
        # test default
        self.assertEqual(Arguments([]).verbose_level, logging.WARNING)

        # test long version
        args = Arguments(['--verbose'])
        self.assertEqual(Arguments(['--verbose']).verbose_level, logging.INFO)

        # test short version
        self.assertEqual(Arguments(['-v']).verbose_level, logging.INFO)

        # test multiple
        self.assertEqual(Arguments(['-vv']).verbose_level, logging.DEBUG)

        # test max
        self.assertEqual(Arguments(['-vvv']).verbose_level, logging.DEBUG)

    def test_dry_run(self):
        self.assertFalse(Arguments([]).dry_run)
        self.assertTrue(Arguments(['--dry-run']).dry_run)
