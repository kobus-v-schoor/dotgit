import os


class Plugin:
    def __init__(self, pre_dir, post_dir, data_dir):
        self.pre_dir = pre_dir
        self.post_dir = post_dir
        self.data_dir = data_dir

        if os.path.isdir(self.data_dir):
            self.setup_data()

    def create_dirs(self, parent, path):
        dirname = os.path.join(parent, os.path.dirname(path))
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

    def setup_data(self):
        pass

    def apply(self, path):
        pass

    def remove(self, path):
        pass
