import enum


class Actions(enum.Enum):
    INIT = 'init'
    UPDATE = 'update'
    RESTORE = 'restore'
    CLEAN = 'clean'
    DIFF = 'diff'
    REPO_CLEANUP = 'repo-clean'
