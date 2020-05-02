import pytest
import os
import subprocess
import shlex

@pytest.fixture(scope='session', autouse=True)
def setup_git_user():
    run = lambda cmd: subprocess.run(shlex.split(cmd),
            stdout=subprocess.PIPE).stdout.decode().strip()

    if not run('git config user.name'):
        run('git config --global user.name "Test User"')
    if not run('git config user.email'):
        run('git config --global user.email "test@example.org"')
