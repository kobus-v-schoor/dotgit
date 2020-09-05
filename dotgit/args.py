import logging
import argparse

from dotgit.enums import Actions
import dotgit.info as info
import dotgit.help

HELP = {
    'verbose': 'print more info to the console',
    'dry-run': 'do not actually execute any file operations',
    'hard-mode': 'copy files instead of symlinking them',
    'action': 'action to take on active categories',
    'category': 'categories to activate. (default: %(default)s)'
}


class Arguments:
    def __init__(self, args=None):
        # construct parser
        formatter = argparse.RawDescriptionHelpFormatter
        parser = argparse.ArgumentParser(epilog=dotgit.help.HELP,
                                         formatter_class=formatter)

        # add parser options
        parser.add_argument('--version', action='version',
                            version=f'dotgit {info.__version__}')
        parser.add_argument('--verbose', '-v', action='count', default=0,
                            help=HELP['verbose'])
        parser.add_argument('--dry-run', action='store_true',
                            help=HELP['dry-run'])
        parser.add_argument('--hard', action='store_true',
                            help=HELP['hard-mode'])

        parser.add_argument('action', choices=[a.value for a in Actions],
                            help=HELP['action'])
        parser.add_argument('category', nargs='*',
                            default=['common', info.hostname],
                            help=HELP['category'])

        # parse args
        args = parser.parse_args(args)

        # extract settings
        if args.verbose:
            args.verbose = min(args.verbose, 2)
            self.verbose_level = (logging.INFO if args.verbose < 2 else
                                  logging.DEBUG)
        else:
            self.verbose_level = logging.WARNING

        self.dry_run = args.dry_run
        self.hard_mode = args.hard
        self.action = Actions(args.action)
        self.categories = args.category

    def __str__(self):
        return str(vars(self))
