import os
import logging
import subprocess


def safety_checks(dir_name, home, init):
    # check that we're not in the user's home folder
    if dir_name == home:
        logging.error('dotgit should not be run inside home folder')
        return False

    try:
        subprocess.run(['git', '--version'], check=True,
                       stdout=subprocess.PIPE)
    except FileNotFoundError:
        logging.error('"git" command not found in path, needed for proper '
                      'dotgit operation')
        return False

    if init:
        return True

    if os.path.isfile(os.path.join(dir_name, 'cryptlist')):
        logging.error('this appears to be an old dotgit repo, please check '
                      'the user guide on how to update this repo for the '
                      'new version of dotgit')
        return False

    if not os.path.isdir(os.path.join(dir_name, '.git')):
        logging.error('''this does not appear to be a git repo, make sure to
        init the repo before running dotgit in this folder''')
        return False

    for flist in ['filelist']:
        if not os.path.isfile(os.path.join(dir_name, flist)):
            logging.error(f'unable to locate {flist} in repo')
            return False

    return True
