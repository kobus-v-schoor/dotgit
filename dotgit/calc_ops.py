import os
import logging

from dotgit.file_ops import FileOps

class CalcOps:
    def __init__(self, repo, restore_path):
        self.repo = repo
        self.restore_path = restore_path

    def update(self, files):
        fops = FileOps(self.repo)

        for path in files:
            categories = files[path]

            master = min(categories)
            slaves = [c for c in categories if c != master]

            # search through home folder and all categories for viable file
            # candidates
            candidates = set()
            search = [self.restore_path]
            search += [os.path.join(self.repo,c) for c in categories]
            for cand in search:
                cand = os.path.join(cand, path)
                if os.path.isfile(cand):
                    if os.path.islink(cand):
                        cand = os.path.realpath(cand)
                    candidates.add(cand)

            if not candidates:
                logging.warning(f'unable to find any candidates for "{path}"')
                continue

            if len(candidates) > 1:
                print(f'multiple candidates found for {path}:\n')

                for i, cand in enumerate(candidates):
                    print(f'[{i}] {cand}')
                print('[-1] cancel')

                while True:
                    try:
                        choice = int(input('please select the version you '
                            f'would like to use: 0-{len(candidates)-1}'))
                        choice = candidates[choice]
                    except:
                        print('invalid choice entered, please try again')
                        continue
                    break
                source = choice
            else:
                source = candidates.pop()

            master = os.path.join(self.repo, master, path)
            slaves = [os.path.join(self.repo, s, path) for s in slaves]
            if source != master:
                if os.path.exists(master):
                    fops.remove(master)
                fops.move(source, master)

            for slave in slaves:
                if slave != source:
                    if os.path.isfile(slave) or os.path.islink(slave):
                        if os.path.realpath(slave) != master:
                            fops.remove(slave)
                        else:
                            # already linked to master so just ignore
                            continue
                fops.link(master, slave)

        return fops

    def restore(self, files, hard=False):
        fops = FileOps(self.repo)

        for path in files:
            categories = files[path]
            master = min(categories)
            source = os.path.join(self.repo, master, path)

            if not os.path.exists(source):
                logging.debug(f'{source} not found in repo')
                logging.warning(f'unable to find "{path}" in repo, skipping')
                continue

            dest = os.path.join(self.restore_path, path)

            if os.path.exists(dest):
                if os.path.samefile(source, dest):
                    logging.debug(f'{dest} already linked to repo, skipping')
                    continue

                a = input(f'{dest} already exists, replace? [Yn] ')
                a = 'y' if not a else a
                if a.lower() == 'y':
                    fops.remove(dest)
                else:
                    continue

            if hard:
                fops.copy(source, dest)
            else:
                fops.link(source, dest)

        return fops

    def clean(self, files, hard=False):
        fops = FileOps(self.repo)

        for path in files:
            path = os.path.join(self.restore_path, path)

            if hard:
                if os.path.isfile(path):
                    fops.remove(path)
            else:
                if (os.path.islink(path) and
                        os.path.realpath(path).startswith(self.repo)):
                    fops.remove(path)

        return fops
