import os
import logging
import enum

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
        dirname =  os.path.dirname(path)
        if not os.path.isdir(self.check_path(dirname)):
            self.mkdir(dirname)
            return True
        return False

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

    def apply(self):
        pass

    def __str__(self):
        fin = []
        for opt in self.ops:
            op, path = opt
            if type(path) is tuple:
                fin.append(f'{op.name} "{path[0]}" -> "{path[1]}"')
            else:
                fin.append(f'{op.name} "{path}"')
        return '\n'.join(fin)
