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

                # group
                if '=' in line:
                    group, categories = line.split('=')
                    categories = categories.split(',')
                    self.groups[group] = categories
                # file
                else:
                    line = line.split(':')
                    path, categories, plugins = line[0], ['common'], ['plain']
                    if len(line) > 1:
                        categories = line[1].split(',')
                    if len(line) > 2:
                        plugins = line[2].split(',')

                    if path not in self.files:
                        self.files[path] = []
                    self.files[path].append({
                        'categories': categories,
                        'plugins': plugins
                    })

    def activate(self, categories):
        # expand groups
        categories = [self.groups.get(c, [c]) for c in categories]
        # flatten category list
        categories = [c for cat in categories for c in cat]

        files = {}
        for path in self.files:
            for group in self.files[path]:
                cat_list = group['categories']
                if set(categories) & set(cat_list):
                    if path in files:
                        logging.error('multiple category lists active for '
                                      f'{path}: {files[path]["categories"]} '
                                      f'and {cat_list}')
                        raise RuntimeError
                    else:
                        files[path] = group

        return files
