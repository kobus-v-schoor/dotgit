import logging

from dotgit.args import Arguments

class TestArguments:
    def test_verbose(self):
        # test default
        assert Arguments([]).verbose_level == logging.WARNING

        # test long version
        assert Arguments(['--verbose']).verbose_level == logging.INFO

        # test short version
        assert Arguments(['-v']).verbose_level == logging.INFO

        # test multiple
        assert Arguments(['-vv']).verbose_level == logging.DEBUG

        # # test max
        assert Arguments(['-vvv']).verbose_level == logging.DEBUG

    def test_dry_run(self):
        assert not Arguments([]).dry_run
        assert Arguments(['--dry-run']).dry_run
