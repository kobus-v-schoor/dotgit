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
    def samefile(self, repo_file, ext_file):
        if self.hard:
            if os.path.islink(ext_file):
                return False
            if not os.path.exists(repo_file):
                return False
            return filecmp.cmp(repo_file, ext_file, shallow=False)
        else:
            # not using os.samefile since it resolves repo_file as well which
            # is not what we want
            return os.path.realpath(ext_file) == os.path.abspath(repo_file)

    def strify(self, op):
        if op == self.apply:
            return "COPY"
        elif op == self.remove:
            return "COPY" if self.hard else "LINK"
        return ""
