import os
import shutil

from dotgit.plugin import Plugin


class PlainPlugin(Plugin):
    def setup_data(self):
        pass

    def apply(self, source, dest):
        shutil.copyfile(source, dest)

    def remove(self, source, dest):
        os.symlink(source, dest)

    def samefile(self, file1, file2):
        return os.path.samefile(file1, file2)
