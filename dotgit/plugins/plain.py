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

    # copies file from outside the repo to the repo
    def apply(self, source, dest):
        shutil.copy2(source, dest)

    # if not in hard mode, creates a symlink in dest (outside the repo) that
    # points to source (inside the repo)
    # if in hard mode, copies the file from the repo to the dest.
    def remove(self, source, dest):
        if self.hard:
            shutil.copy2(source, dest)
        else:
            os.symlink(source, dest)

    # if not in hard mode, checks if symlink points to file in repo
    # if in hard mode, a bit-by-bit comparison is made to compare the files
    def samefile(self, file1, file2):
        if self.hard:
            return filecmp.cmp(file1, file2, shallow=False)
        else:
            return os.path.samefile(file1, file2)

    def strify(self, op):
        if op == self.apply:
            return "COPY"
        elif op == self.remove:
            return "COPY" if self.hard else "LINK"
        return ""
