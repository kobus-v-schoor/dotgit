import os
from dotgit.plugin import Plugin


class PlainPlugin(Plugin):
    def setup_data(self):
        pass

    def apply(self, path):
        self.create_dirs(self.post_dir, path)
        os.symlink(os.path.join(self.pre_dir, path),
                   os.path.join(self.post_dir, path))

    def remove(self, path):
        self.create_dirs(self.pre_dir, path)
        os.rename(os.path.join(self.post_dir, path),
                  os.path.join(self.pre_dir, path))
        self.apply(path)
