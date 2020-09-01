import os
import subprocess

import pytest

from dotgit.git import Git, FileState

class TestGit:
    def touch(self, folder, fname):
        open(os.path.join(folder, fname), 'w').close()

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

    def setup_git(self, tmp_path):
        repo = os.path.join(tmp_path, 'repo')
        os.makedirs(repo)

        git = Git(repo)
        git.init()

        return git, repo

    def test_reset_all(self, tmp_path):
        git, repo = self.setup_git(tmp_path)
        self.touch(repo, 'file')
        self.touch(repo, 'file2')
        assert git.status()==[(FileState.UNTRACKED,f) for f in ['file','file2']]
        git.add()
        assert git.status()==[(FileState.ADDED,f) for f in ['file','file2']]
        git.reset()
        assert git.status()==[(FileState.UNTRACKED,f) for f in ['file','file2']]

    def test_reset_file(self, tmp_path):
        git, repo = self.setup_git(tmp_path)
        self.touch(repo, 'file')
        self.touch(repo, 'file2')
        assert git.status()==[(FileState.UNTRACKED,f) for f in ['file','file2']]
        git.add()
        assert git.status()==[(FileState.ADDED,f) for f in ['file','file2']]
        git.reset('file')
        assert git.status()==[(FileState.UNTRACKED, 'file'), (FileState.ADDED,
            'file2')]

    def test_add_all(self, tmp_path):
        git, repo = self.setup_git(tmp_path)
        self.touch(repo, 'file')
        self.touch(repo, 'file2')
        assert git.status()==[(FileState.UNTRACKED,f) for f in ['file','file2']]
        git.add()
        assert git.status()==[(FileState.ADDED,f) for f in ['file','file2']]

    def test_add_file(self, tmp_path):
        git, repo = self.setup_git(tmp_path)
        self.touch(repo, 'file')
        self.touch(repo, 'file2')
        assert git.status()==[(FileState.UNTRACKED,f) for f in ['file','file2']]
        git.add('file')
        assert git.status()==[(FileState.ADDED, 'file'), (FileState.UNTRACKED,
            'file2')]

    def test_commit_msg(self, tmp_path):
        git, repo = self.setup_git(tmp_path)
        self.touch(repo, 'file')
        git.add('file')
        msg = 'commit message with "quotes"'
        git.commit(msg)
        proc = subprocess.run(['git', 'log', '-1', '--pretty=%s'], cwd=repo,
                stdout=subprocess.PIPE).stdout.decode().strip()
        assert proc == msg

    def test_commit_no_msg(self, tmp_path):
        git, repo = self.setup_git(tmp_path)
        self.touch(repo, 'file')
        git.add('file')
        git.commit()
        proc = subprocess.run(['git', 'log', '-1', '--pretty=%s'], cwd=repo,
                stdout=subprocess.PIPE).stdout.decode().strip()
        assert proc == 'Added file'

    def test_gen_commit_msg(self, tmp_path):
        git, repo = self.setup_git(tmp_path)
        self.touch(repo, 'new')
        self.touch(repo, 'new2')
        git.add()
        self.touch(repo, 'new3')
        assert git.gen_commit_message() == 'Added new, added new2'

    def test_status_untracked(self, tmp_path):
        git, repo = self.setup_git(tmp_path)
        self.touch(repo, 'untracked')
        assert git.status() == [(FileState.UNTRACKED, 'untracked')]

    def test_status_tracked(self, tmp_path):
        git, repo = self.setup_git(tmp_path)
        self.touch(repo, 'tracked')
        git.add('tracked')
        assert git.status() == [(FileState.ADDED, 'tracked')]

    # tests stage/working tree switch as well
    def test_status_added_deleted(self, tmp_path):
        git, repo = self.setup_git(tmp_path)
        self.touch(repo, 'delete')
        git.add('delete')
        os.remove(os.path.join(repo, 'delete'))
        git.status()
        assert git.status() == [(FileState.ADDED, 'delete')]
        assert git.status(staged=False) == [(FileState.DELETED, 'delete')]

    def test_status_renamed(self, tmp_path):
        git, repo = self.setup_git(tmp_path)
        with open(os.path.join(repo, 'rename'), 'w') as f:
            f.write('file content\n')
        git.add('rename')
        git.commit()
        os.rename(os.path.join(repo, 'rename'), os.path.join(repo, 'renamed'))
        git.add()
        assert git.status() == [(FileState.RENAMED, 'rename -> renamed')]

    def test_has_changes(self, tmp_path):
        git, repo = self.setup_git(tmp_path)
        assert not git.has_changes()
        self.touch(repo, 'foo')
        assert git.has_changes()
        git.add('foo')
        assert git.has_changes()
        git.commit()
        assert not git.has_changes()

    def test_diff(self, tmp_path):
        git, repo = self.setup_git(tmp_path)
        self.touch(repo, 'foo')
        assert git.diff() == ['added foo']

    def test_diff_no_changes(self, tmp_path):
        git, repo = self.setup_git(tmp_path)
        assert git.diff() == ['no changes']
