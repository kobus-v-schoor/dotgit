import os


class Plugin:
    def __init__(self, data_dir):
        self.data_dir = data_dir

        if os.path.isdir(self.data_dir):
            self.setup_data()

    def setup_data(self):
        pass

    def apply(self, source, dest):
        pass

    def remove(self, source, dest):
        pass

    def samefile(self, file1, file2):
        pass
