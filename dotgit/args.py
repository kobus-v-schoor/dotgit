import logging
import argparse

class Arguments:
    def __init__(self, args=None):
        # construct parser
        parser = argparse.ArgumentParser()

        # add parser options
        parser.add_argument('--verbose', '-v', action='count', default=0)

        # parse args
        args = parser.parse_args(args)

        # extract settings
        if args.verbose:
            args.verbose = min(args.verbose, 2)
            self.verbose_level = [logging.INFO, logging.DEBUG][args.verbose-1]
        else:
            self.verbose_level = logging.WARNING
