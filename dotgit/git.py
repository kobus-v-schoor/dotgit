import os
import subprocess
import shlex
import logging

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
            subprocess.run(cmd, cwd=self.repo_dir, stdout=subprocess.PIPE,
                    check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f'git command {cmd} failed with exit code '
                    f'{e.returncode}')
            logging.error(e.stdout.decode())
            raise
        logging.debug(f'git command {cmd} succeeded')

    def init(self):
        self.run('git init')
