import os
import subprocess

import pytest

from dotgit.git import Git

class TestGit:
    def test_init(self, tmp_path):
        path = os.path.join(tmp_path, 'nonexistent')
        # check that using a non-existent path fails
        with pytest.raises(FileNotFoundError):
            git = Git(path)

    def test_run(self, tmp_path):
        # check than an invalid command fails correctly
        with pytest.raises(subprocess.CalledProcessError):
            Git(tmp_path).run('git status')

    def test_repo_init(self, tmp_path):
        path = os.path.join(tmp_path, 'repo')
        os.makedirs(path)
        git = Git(path)
        git.init()
        # check that a .git folder was created
        assert os.path.isdir(os.path.join(path, '.git'))
        # check that a valid git repo was created
        assert subprocess.run(['git', 'status'], cwd=path).returncode == 0
