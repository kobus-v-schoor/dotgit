import os
import logging

from dotgit.file_ops import FileOps


class CalcOps:
    def __init__(self, repo, restore_path, plugin):
        self.repo = str(repo)
        self.restore_path = str(restore_path)
        self.plugin = plugin

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
            search += [os.path.join(self.repo, c) for c in categories]
            original_path = {}
            for cand in search:
                cand = os.path.join(cand, path)
                if os.path.isfile(cand):
                    if os.path.islink(cand):
                        old = cand
                        cand = os.path.realpath(cand)
                        original_path[cand] = old
                    candidates.add(cand)

            if not candidates:
                logging.warning(f'unable to find any candidates for "{path}"')
                continue

            if len(candidates) > 1:
                candidates = list(candidates)
                print(f'multiple candidates found for {path}:\n')

                for i, cand in enumerate(candidates):
                    print(f'[{i}] {cand}')
                print('[-1] cancel')

                while True:
                    try:
                        choice = int(input('please select the version you '
                                           'would like to use '
                                           f'[0-{len(candidates)-1}]: '))
                        choice = candidates[choice]
                    except (ValueError, EOFError):
                        print('invalid choice entered, please try again')
                        continue
                    break
                source = choice

                # if one of the candidates is not in the repo and it is not the
                # source it should be deleted manually since it will not be
                # deleted in the slave linking below, as the other candidates
                # would be
                restore_path = os.path.join(self.restore_path, path)
                if restore_path in candidates and source != restore_path:
                    fops.remove(restore_path)

            else:
                source = candidates.pop()

            master = os.path.join(self.repo, master, path)
            slaves = [os.path.join(self.repo, s, path) for s in slaves]
            if source != master:
                if os.path.exists(master):
                    fops.remove(master)
                # check if source is in repo, if it is not apply the plugin
                if source.startswith(self.repo + os.sep):
                    # if the source is one of the slaves, move the source
                    # otherwise just copy it because it might have changed into
                    # a seperate category - cleanup will remove it if needed
                    if source in slaves:
                        fops.move(source, master)
                    else:
                        fops.copy(source, master)
                else:
                    fops.plugin(self.plugin.apply, source, master)
                    if source in original_path:
                        fops.remove(original_path[source])
                    else:
                        fops.remove(source)

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

    def restore(self, files):
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
                if self.plugin.samefile(source, dest):
                    logging.debug(f'{dest} already linked to repo, skipping')
                    continue

                # check if the dest is already a symlink to the repo, if it is
                # just remove it without asking
                if os.path.realpath(dest).startswith(self.repo):
                    logging.info(f'{dest} already linked to repo, replacing '
                                 'with new file')
                    fops.remove(dest)
                else:
                    a = input(f'{dest} already exists, replace? [Yn] ')
                    a = 'y' if not a else a
                    if a.lower() == 'y':
                        fops.remove(dest)
                    else:
                        continue
            # check if the destination is a dangling symlink, if it is just
            # remove it
            elif os.path.islink(dest):
                fops.remove(dest)

            fops.plugin(self.plugin.remove, source, dest)

        return fops

    # removes links from restore path that point to the repo
    def clean(self, files):
        fops = FileOps(self.repo)

        for path in files:
            categories = files[path]
            master = min(categories)
            repo_path = os.path.join(self.repo, master, path)

            restore_path = os.path.join(self.restore_path, path)

            if os.path.exists(repo_path) and os.path.exists(restore_path):
                if self.plugin.samefile(repo_path, restore_path):
                    fops.remove(restore_path)

        return fops

    # will go through the repo and search for files that should no longer be
    # there. accepts a list of filenames that are allowed
    def clean_repo(self, filenames):
        fops = FileOps(self.repo)

        if not os.path.isdir(self.repo):
            return fops

        for category in os.listdir(self.repo):
            category_path = os.path.join(self.repo, category)

            # remove empty category folders
            if not os.listdir(category_path):
                logging.info(f'{category} is empty, removing')
                fops.remove(category)
                continue

            for root, dirs, files in os.walk(category_path):
                # remove empty directories
                for dname in dirs:
                    dname = os.path.join(root, dname)
                    if not os.listdir(dname):
                        dname = os.path.relpath(dname, self.repo)
                        logging.info(f'{dname} is empty, removing')
                        fops.remove(dname)

                # remove files that are not in the manifest
                for fname in files:
                    fname = os.path.relpath(os.path.join(root, fname),
                                            self.repo)
                    if fname not in filenames:
                        logging.info(f'{fname} is not in the manifest, '
                                     'removing')
                        fops.remove(fname)

        return fops
