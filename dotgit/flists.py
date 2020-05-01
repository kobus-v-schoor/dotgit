class Filelist:
    def __init__(self, fname):
        self.groups = {}
        self.files = {}

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
