from os.path import expanduser

import dotgit.info

class TestInfo:
    def test_home(self):
        assert dotgit.info.home == expanduser('~')
