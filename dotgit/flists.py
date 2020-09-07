import logging
import os
import re


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
                    split = re.split('[:|]', line)

                    path, categories, plugin = split[0], ['common'], 'plain'
                    if len(split) >= 2:
                        if ':' in line:
                            categories = split[1].split(',')
                        else:
                            plugin = split[1]
                    if len(split) >= 3:
                        plugin = split[2]

                    if path not in self.files:
                        self.files[path] = []
                    self.files[path].append({
                        'categories': categories,
                        'plugin': plugin
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

    # generates a list of all the filenames in each plugin for later use when
    # cleaning the repo
    def manifest(self):
        manifest = {}

        for path in self.files:
            for instance in self.files[path]:
                plugin = instance['plugin']
                for category in instance['categories']:
                    if category in self.groups:
                        categories = self.groups[category]
                    else:
                        categories = [category]

                    if plugin not in manifest:
                        manifest[plugin] = []

                    for category in categories:
                        manifest[plugin].append(os.path.join(category, path))

        return manifest
