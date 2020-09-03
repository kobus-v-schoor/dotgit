import os


class Plugin:
    def __init__(self, data_dir):
        self.data_dir = data_dir

        if os.path.isdir(self.data_dir):
            self.setup_data()

    def setup_data(self):
        pass

    # takes a source (outside the repo) and applies its operation and store the
    # resulting file in dest (inside the repo). This operation should not
    # remove the source file
    def apply(self, source, dest):
        pass

    # takes a source (inside the repo) and removes its operation and stores the
    # result in dest (outside the repo)
    def remove(self, source, dest):
        pass

    def samefile(self, file1, file2):
        pass

    # takes a callable (one of the plugin's ops) and returns a string
    # describing the op
    def strify(self, op):
        pass
