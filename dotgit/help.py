HELP = '''
INITIAL SETUP:
    If you are planning on storing your dotfiles somewhere online, create a
    repository on your chosen platform and clone it to where you intend to
    store your dotfiles. Otherwise, create a directory to store your dotfiles
    and run 'dotgit init' inside of it (you should also run this inside a
    freshly cloned repo)

FILELIST SYNTAX:
    Your filelist is where you will specify what dotfiles you want to store
    inside your dotgit repository. It is located in the root of your dotfiles
    repo with the name "filelist".

    Blank lines are ignored, and lines starting with "#" are comments which are
    also ignored.

    An example filelist might look something like this:

    # this is a comment
    file_name:category1,category2
    second_file

    "file_name" can contain spaces and can be any file or folder inside your
    home directory. You need to specify the file's name relative to your home
    folder, i.e. ".bashrc" for your bash config.

    Categories allow you to group files together to make it easy to manipulate
    them as a group. If no category is specified for a file it is automatically
    added to the "common" category. When you specify multiple categories for a
    file (like above) the file is shared between the categories, meaning
    changes to the file in the one category also affects the other. You can
    also use categories to separate different versions of the same file, for
    instance:

    .vimrc:server
    .vimrc:workstation

    Category groups allow you to group multiple categories together. Their
    syntax looks as follows:

    group_name=category1,category2

    This makes it even easier to manage groups of dotfiles. You can use groups
    and categories any way you like, but one approach tends to work very well.
    It looks as follows:

    server=vim,shell
    workstation=x,vim,shell

    .vimrc:vim
    .bashrc:shell
    .xinitrc:x

    In the example above, you separate your dotfiles into categories that
    groups similar dotfiles (e.g. all your vim-related dotfiles in one
    category). Next, you create groups that matches the hostnames of the
    machines that you intend to use it on. The groups then contain all the
    categories you want to use on that machines. Using this method allows you
    to easily add and remove categories on your hosts almost like they are
    packages.

    Note that if you run dotgit commands without specifying any categories,
    dotgit automatically assumes the "common" category as well as a category
    with your hostname (e.g. "kobus-laptop"). This means that if you use groups
    (or categories) that match the hostnames you want to use dotgit on you
    don't need to specify any categories when running dotgit as your hostname
    already matches the correct categories.

OPTIONS:

    usage: dotgit   [-h] [--verbose] [--dry-run] [--hard] {action}
                    [category [category ...]]

    If you don't add any categories after your action, two categories, "common"
    and your hostname will be implicitly added. When you add categories only
    the files that are in those categories will be taken into consideration.
    For instance, if you specify "c1" after "update" only files marked with the
    "c1" category will be updated.

    It is recommended that you run dotgit with verbose mode (-v) to see what is
    happening. You can also run dotgit with "--dry-run" to prevent any changes
    to your filesystem if you want to check what dotgit would have done.

    init           - setup a new dotgit repository inside the current directory

    update         - run this only after you changed your filelist. This will
                     update the repository structure to match your filelist. Do
                     not use this if you only modified your dotfiles, it is
                     unnecessary. If you run dotgit in symlink mode take note
                     that running update will delete the original file inside
                     your home folder and replace it with a link to the
                     repository automatically.

    restore        - creates links in your home folder pointing to your
                     repository. You need to run this whenever you want to
                     setup a new machine or if you made changes to the filelist
                     on another machine and you want the changes to be added to
                     the current machine.

    clean          - This will remove all links in your home folder that point
                     to your dotfiles repository

    diff           - This will print your current changes in your dotfiles
                     repository

    commit         - This will generate a git commit message and push to a
                     remote if it can find one (will ask for confirmation)

    The 'update', 'restore' and 'clean' actions have a 'hard' mode, activated
    by using the --hard flag. When in this mode dotgit will copy the files
    to/from the repository rather than symlinking it.  In the case of 'clean'
    it will also remove files (that match the files inside the repo) and not
    just symlinks. This can be useful if you want to for example clone the
    repository onto a machine, restore your dotfiles and then delete the
    repository again.
'''
