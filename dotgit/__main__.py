#! /usr/bin/env python3

import logging
import sys
import os

# add the directory which contains the dotgit module to the path. this will
# only ever execute when running the __main__.py script directly since the
# python package will use an entrypoint
if __name__ == '__main__':
    import site
    mod = os.path.dirname(os.path.realpath(__file__))
    site.addsitedir(os.path.dirname(mod))

from dotgit.args import Arguments
from dotgit.enums import Actions
from dotgit.checks import safety_checks
from dotgit.git import Git
import dotgit.info as info


def init_repo(repo_dir, flist):
    git = Git(repo_dir)
    if not os.path.isdir(os.path.join(repo_dir, '.git')):
        logging.info('creating git repo')
        git.init()
    else:
        logging.warning('existing git repo, not re-creating')

    changed = False

    if not os.path.isfile(flist):
        logging.info('creating empty filelist')
        open(flist, 'w').close()
        git.add(os.path.basename(flist))
        changed = True
    else:
        logging.warning('existing filelist, not recreating')

    gitignore = os.path.join(repo_dir, '.gitignore')
    if not os.path.isfile(gitignore):
        logging.info('creating gitignore')
        with open(gitignore, 'w') as f:
            f.write('.plugins/*/pre\n.plugins/*/post\n')
        git.add('.gitignore')
        changed = True
    else:
        logging.warning('existing .gitignore, not re-creating')

    if changed:
        git.commit()


def main(args=None, cwd=os.getcwd(), home=info.home):
    if args is None:
        args = sys.argv[1:]

    # parse cmd arguments
    args = Arguments(args)
    logging.basicConfig(format='%(message)s ', level=args.verbose_level)
    logging.debug(f'ran with arguments {args}')

    repo = cwd
    flist_fname = os.path.join(repo, 'filelist')

    # run safety checks
    if not safety_checks(repo, home, args.action == Actions.INIT):
        logging.error(f'safety checks failed for {os.getcwd()}, exiting')
        return 1

    if args.action == Actions.INIT:
        init_repo(repo, flist_fname)
        return 0

    return 0


if __name__ == '__main__':
    sys.exit(main())
