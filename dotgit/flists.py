import logging

class Filelist:
    def __init__(self, fname):
        self.groups = {}
        self.files = {}

        logging.debug(f'parsing filelist in {fname}')

        with open(fname, 'r') as f:
            for line in f.readlines():
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                # common file
                if not '=' in line and not ':' in line:
                    line = f'{line}:common'

                # group
                if '=' in line:
                    group, categories = line.split('=')
                    categories = categories.split(',')
                    self.groups[group] = categories
                # file
                elif ':' in line:
                    path, categories = line.split(':')
                    categories = categories.split(',')
                    if not path in self.files:
                        self.files[path] = []
                    self.files[path].append(categories)

    def activate(self, categories):
        # expand groups
        categories = [self.groups.get(c, [c]) for c in categories]
        # flatten category list
        categories = [c for cat in categories for c in cat]

        files = {}
        for path in self.files:
            for cat_list in self.files[path]:
                if set(categories) & set(cat_list):
                    if path in files:
                        logging.error('multiple category lists active for '
                                f'{path}: {files[path]} and {cat_list}')
                        raise RuntimeError
                    else:
                        files[path] = cat_list

        return files
