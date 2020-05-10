import os
import logging
import subprocess

import dotgit.info as info
from dotgit.enums import Actions


def safety_checks(dir_name: str, action: Actions) -> bool:
    # check that we're not in the user's home folder
    if dir_name == info.home:
        logging.error('dotgit should not be run inside home folder')
        return False

    try:
        subprocess.run(['git', '--version'], check=True,
                         stdout=subprocess.PIPE)
    except FileNotFoundError:
        logging.error('"git" command not found in path, needed for proper '
                      'dotgit operation')
        return False

    if action == Actions.INIT:
        return True

    if not os.path.isdir(os.path.join(dir_name, '.git')):
        logging.error('''this does not appear to be a git repo, make sure to
        init the repo before running dotgit in this folder''')
        return False

    for flist in ['filelist']:
        if not os.path.isfile(os.path.join(dir_name, flist)):
            logging.error(f'unable to locate {flist} in repo')
            return False

    return True
