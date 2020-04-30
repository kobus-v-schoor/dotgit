import os

from dotgit.checks import safety_checks
from dotgit.enums import Actions
import dotgit.info as info

class TestSafetyChecks:
    def test_checks(self, tmp_path):
        # check that running in home fails
        assert not safety_checks(info.home, Actions.INIT)

        # check that using init in empty dir is fine
        assert safety_checks(tmp_path, Actions.INIT)

        # check that is passes if git and filelist is there
        git = os.path.join(tmp_path, '.git')
        flist = os.path.join(tmp_path, 'filelist')

        create_git = lambda : os.makedirs(git)
        create_flist = lambda : open(flist, 'w').close()

        # check for fail in empty folder for non-init action
        assert not safety_checks(tmp_path, Actions.UPDATE)

        # check for pass with git and filelist
        create_git()
        create_flist()
        assert safety_checks(tmp_path, Actions.UPDATE)

        # check for git fail
        os.rmdir(git)
        assert not safety_checks(tmp_path, Actions.UPDATE)

        # check for filelist fail
        create_git()
        os.remove(flist)
        assert not safety_checks(tmp_path, Actions.UPDATE)
