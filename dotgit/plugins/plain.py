import os
import shutil
import filecmp

from dotgit.plugin import Plugin


class PlainPlugin(Plugin):
    def __init__(self, *args, **kwargs):
        self.hard = kwargs.pop('hard', False)
        super().__init__(*args, **kwargs)

    def setup_data(self):
        pass

    def apply(self, source, dest):
        shutil.copyfile(source, dest)

    def remove(self, source, dest):
        if self.hard:
            shutil.copyfile(source, dest)
        else:
            os.symlink(source, dest)

    def samefile(self, file1, file2):
        if self.hard:
            return filecmp.cmp(file1, file2, shallow=False)
        else:
            return os.path.samefile(file1, file2)
