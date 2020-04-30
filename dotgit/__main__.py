#! /usr/bin/env python3

import logging
import sys
import os

# add the directory which contains the dotgit module to the path. this will only
# ever execute when running the __main__.py script directly since the python
# package will use an entrypoint
if __name__ == '__main__':
    import site
    mod = os.path.dirname(os.path.realpath(__file__))
    site.addsitedir(os.path.dirname(mod))

from dotgit.args import Arguments
from dotgit.checks import safety_checks

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    # parse cmd arguments
    args = Arguments(args)
    logging.basicConfig(format='%(message)s ', level=args.verbose_level)
    logging.debug(f'ran with arguments {args}')

    # run safety checks
    if not safety_checks(os.getcwd(), args.action):
        logging.error(f'safety checks failed for {os.getcwd()}, exiting')
        sys.exit(1)

if __name__ == '__main__':
    main()
