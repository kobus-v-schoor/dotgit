import unittest

import logging

from dotgit.args import Arguments

class ArgumentsTests(unittest.TestCase):
    def test_verbose(self):
        # test default
        args = Arguments([])
        self.assertEqual(args.verbose_level, logging.WARNING)

        # test long version
        args = Arguments(['--verbose'])
        self.assertEqual(args.verbose_level, logging.INFO)

        # test short version
        args = Arguments(['-v'])
        self.assertEqual(args.verbose_level, logging.INFO)

        # test multiple
        args = Arguments(['-vv'])
        self.assertEqual(args.verbose_level, logging.DEBUG)

        # test max
        args = Arguments(['-vvv'])
        self.assertEqual(args.verbose_level, logging.DEBUG)
