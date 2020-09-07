import os
import subprocess
import shlex
import logging
import enum


class FileState(enum.Enum):
    MODIFIED = 'M'
    ADDED = 'A'
    DELETED = 'D'
    RENAMED = 'R'
    COPIED = 'C'
    UPDATED = 'U'
    UNTRACKED = '?'


class Git:
    def __init__(self, repo_dir):
        if not os.path.isdir(repo_dir):
            raise FileNotFoundError

        self.repo_dir = repo_dir

    def run(self, cmd):
        if not type(cmd) is list:
            cmd = shlex.split(cmd)
        logging.info(f'running git command {cmd}')
        try:
            proc = subprocess.run(cmd, cwd=self.repo_dir,
                                  stdout=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(e.stdout.decode())
            logging.error(f'git command {cmd} failed with exit code '
                          f'{e.returncode}\n')
            raise
        logging.debug(f'git command {cmd} succeeded')
        return proc.stdout.decode()

    def init(self):
        self.run('git init')

    def reset(self, fname=None):
        self.run('git reset' if fname is None else f'git reset {fname}')

    def add(self, fname=None):
        self.run('git add --all' if fname is None else f'git add {fname}')

    def commit(self, message=None):
        if message is None:
            message = self.gen_commit_message()
        return self.run(['git', 'commit', '-m', message])

    def status(self, staged=True):
        out = self.run('git status --porcelain').strip()
        status = []
        for line in out.split('\n'):
            state, path = line[:2], line[3:]
            stage, work = state
            status.append((FileState(stage if staged else work), path))
        return sorted(status, key=lambda s: s[1])

    def has_changes(self):
        return bool(self.run('git status -s --porcelain').strip())

    def gen_commit_message(self, ignore=[]):
        mods = []
        for stat in self.status():
            state, path = stat
            # skip all untracked files since they will not be committed
            if state == FileState.UNTRACKED:
                continue
            if any((path.startswith(p) for p in ignore)):
                logging.debug(f'ignoring {path} from commit message')
                continue
            mods.append(f'{state.name.lower()} {path}')
        return ', '.join(mods).capitalize()

    def commits(self):
        return self.run('git log -1 --pretty=%s').strip().split('\n')

    def last_commit(self):
        return self.commits()[-1]

    def has_remote(self):
        return bool(self.run('git remote').strip())

    def push(self):
        self.run('git push')

    def diff(self, ignore=[]):
        if not self.has_changes():
            return ['no changes']

        self.add()
        status = self.status()
        self.reset()

        diff = []

        for path in status:
            # ignore the paths specified in ignore
            if any((path[1].startswith(i) for i in ignore)):
                continue
            diff.append(f'{path[0].name.lower()} {path[1]}')

        return diff
