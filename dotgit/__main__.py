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
from dotgit.flists import Filelist
from dotgit.git import Git
from dotgit.calc_ops import CalcOps
from dotgit.plugins.plain import PlainPlugin
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

    # check for init
    if args.action == Actions.INIT:
        init_repo(repo, flist_fname)
        return 0

    # parse filelist
    filelist = Filelist(flist_fname)
    try:
        filelist = filelist.activate(args.categories)
    except RuntimeError:
        return 1

    # init plugins
    plugins_data_dir = os.path.join(repo, '.plugins')
    plugins = {
        'plain': PlainPlugin(data_dir=os.path.join(plugins_data_dir, 'plain'),
                             hard=args.hard_mode)
    }

    # set up operations
    if args.action == Actions.UPDATE:
        operations = [Actions.UPDATE, Actions.RESTORE, Actions.REPO_CLEANUP]
    elif args.action == Actions.RESTORE:
        operations = [Actions.RESTORE, Actions.REPO_CLEANUP]

    # calculate and apply file operations
    dotfiles = os.path.join(repo, 'dotfiles')

    for plugin in plugins:
        flist = {path: filelist[path]['categories'] for path in filelist if
                 filelist[path]['plugin'] == plugin}
        if not flist:
            continue

        plugin_dir = os.path.join(dotfiles, plugin)
        calc_ops = CalcOps(plugin_dir, home, plugins[plugin])

        for op in operations:
            if op == Actions.UPDATE:
                calc_ops.update(flist).apply(args.dry_run)
            elif op == Actions.RESTORE:
                calc_ops.restore(flist).apply(args.dry_run)

    return 0


if __name__ == '__main__':
    sys.exit(main())
