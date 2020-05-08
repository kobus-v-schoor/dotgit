import os
import logging

from dotgit.file_ops import FileOps

class CalcOps:
    def __init__(self, repo, restore):
        self.repo = repo
        self.restore = restore

    def update(self, files):
        fops = FileOps(self.repo)

        # gonna be using this quite a lot
        join = os.path.join

        for path in files:
            categories = files[path]

            master = min(categories)
            slaves = [c for c in categories if c != master]

            # search through home folder and all categories for viable file
            # candidates
            candidates = set()
            for cand in [self.restore,*[join(self.repo,c) for c in categories]]:
                cand = join(cand, path)
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

            master = join(self.repo, master, path)
            slaves = [join(self.repo, s, path) for s in slaves]
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
