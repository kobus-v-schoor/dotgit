import logging
import socket

from dotgit.args import Arguments
from dotgit.enums import Actions

class TestArguments:
    valid_actions = [a.value for a in Actions]

    def test_verbose(self):
        act = self.valid_actions[0]

        # test default
        assert Arguments([act]).verbose_level == logging.WARNING

        # test long version
        assert Arguments(['--verbose', act]).verbose_level == logging.INFO

        # test short version
        assert Arguments(['-v', act]).verbose_level == logging.INFO

        # test multiple
        assert Arguments(['-vv', act]).verbose_level == logging.DEBUG

        # # test max
        assert Arguments(['-vvv', act]).verbose_level == logging.DEBUG

    def test_dry_run(self):
        act = self.valid_actions[0]

        assert not Arguments([act]).dry_run
        assert Arguments(['--dry-run', act]).dry_run

    def test_hard_mode(self):
        act = self.valid_actions[0]

        assert not Arguments([act]).hard_mode
        assert Arguments(['--hard', act]).hard_mode

    def test_actions(self):
        # test valid actions
        for act in self.valid_actions:
            assert Arguments([act]).action == Actions(act)

    def test_categories(self):
        act = self.valid_actions[0]

        assert Arguments([act]).categories == ['common', socket.gethostname()]
        assert Arguments([act, 'foo']).categories == ['foo']
