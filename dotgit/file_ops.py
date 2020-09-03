import os
import logging
import enum
import shutil
import inspect


class Op(enum.Enum):
    LINK = enum.auto()
    COPY = enum.auto()
    MOVE = enum.auto()
    REMOVE = enum.auto()
    MKDIR = enum.auto()


class FileOps:
    def __init__(self, wd):
        self.wd = wd
        self.ops = []

    def clear(self):
        self.ops = []

    def check_path(self, path):
        return path if os.path.isabs(path) else os.path.join(self.wd, path)

    def check_dest_dir(self, path):
        dirname = os.path.dirname(path)
        if not os.path.isdir(self.check_path(dirname)):
            self.mkdir(dirname)

    def mkdir(self, path):
        logging.debug(f'adding mkdir op for {path}')
        self.ops.append((Op.MKDIR, path))

    def copy(self, source, dest):
        logging.debug(f'adding cp op for {source} -> {dest}')
        self.check_dest_dir(dest)
        self.ops.append((Op.COPY, (source, dest)))

    def move(self, source, dest):
        logging.debug(f'adding mv op for {source} -> {dest}')
        self.check_dest_dir(dest)
        self.ops.append((Op.MOVE, (source, dest)))

    def link(self, source, dest):
        logging.debug(f'adding ln op for {source} <- {dest}')
        self.check_dest_dir(dest)
        self.ops.append((Op.LINK, (source, dest)))

    def remove(self, path):
        logging.debug(f'adding rm op for {path}')
        self.ops.append((Op.REMOVE, path))

    def plugin(self, plugin, source, dest):
        logging.debug(f'adding plugin op ({plugin.__qualname__}) for {source} '
                      f'-> {dest}')
        self.check_dest_dir(dest)
        self.ops.append((plugin, (source, dest)))

    def apply(self, dry_run=False):
        for op in self.ops:
            op, path = op

            if type(path) is tuple:
                src, dest = path
                src, dest = self.check_path(src), self.check_path(dest)
                logging.info(self.str_op(op, (src, dest)))
            else:
                path = self.check_path(path)
                logging.info(self.str_op(op, path))

            if dry_run:
                continue

            if op == Op.LINK:
                src = os.path.relpath(src, os.path.join(self.wd,
                                                        os.path.dirname(dest)))
                os.symlink(src, dest)
            elif op == Op.COPY:
                shutil.copyfile(src, dest)
            elif op == Op.MOVE:
                os.rename(src, dest)
            elif op == Op.REMOVE:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            elif op == Op.MKDIR:
                if not os.path.isdir(path):
                    os.makedirs(path)
            elif callable(op):
                op(src, dest)

        self.clear()

    def append(self, other):
        self.ops += other.ops
        return self

    def str_op(self, op, path):
        def strip_wd(p):
            p = str(p)
            wd = str(self.wd)
            return p[len(wd) + 1:] if p.startswith(wd) else p

        if type(op) is Op:
            op = op.name
        else:
            op = dict(inspect.getmembers(op))['__self__'].strify(op)

        if type(path) is tuple:
            path = [strip_wd(p) for p in path]
            return f'{op} "{path[0]}" -> "{path[1]}"'
        else:
            return f'{op} "{strip_wd(path)}"'

    def __str__(self):
        return '\n'.join(self.str_op(*op) for op in self.ops)

    def __repr__(self):
        return str(self.ops)
