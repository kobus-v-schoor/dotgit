import enum


class Actions(enum.Enum):
    INIT = 'init'

    UPDATE = 'update'
    RESTORE = 'restore'
    CLEAN = 'clean'

    DIFF = 'diff'
    COMMIT = 'commit'

    PASSWD = 'passwd'
