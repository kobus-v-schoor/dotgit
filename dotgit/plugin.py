import os


class Plugin:
    def __init__(self, data_dir, repo_dir=None):
        self.data_dir = data_dir
        self.repo_dir = '/' if repo_dir is None else repo_dir

        if not os.path.isdir(self.data_dir):
            os.makedirs(self.data_dir)

        self.setup_data()

    # does plugin-specific setting up of data located in the data_dir
    def setup_data(self):
        pass

    # cleans up plugin's data by removing entries that is no longer in the
    # given manifest
    def clean_data(self, manifest):
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

    # takes a path to a repo_file and an ext_file and compares them, should
    # return true if they are the same file
    def samefile(self, repo_file, ext_file):
        pass

    # takes a callable (one of the plugin's ops) and returns a string
    # describing the op
    def strify(self, op):
        pass

    # takes a path inside the repo and strips the repo dir as a prefix
    def strip_repo(self, path):
        if os.path.isabs(path):
            return os.path.relpath(path, self.repo_dir)
        return path
