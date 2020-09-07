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
    third_file|encrypt
    fourth_file:category1,category2|encrypt

    "file_name" can contain spaces and can be any file or folder inside your
    home directory. You need to specify the file's name relative to your home
    folder, i.e. ".bashrc" for your bash config.

    Jumping ahead, the third file specifies to use the "encrypt" plugin, which
    encrypts files before saving them in your dotfiles repo. Currently, only
    one plugin is supported (namely the "encrypt" plugin).

    The first file specifies two categories, "category1" and "category2".

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
    and categories any way you like, but the following tends to work very well.
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

EXAMPLE WORKFLOW:

    A typical workflow might look something like the following. In this example
    we will set up two machines to use dotgit. The first will be named "laptop"
    and the second "desktop". We want to share a ".vimrc" file between the two
    but have separate ".xinitrc" files.

    First we start on the laptop. On it we have the ".vimrc" file that we want
    to share as well as the ".xinitrc" file for the laptop. We create a new
    dotgit repo (cloning an empty repo or just making an empty dir) and init
    the repo by running the following inside the repo dir:

    [laptop]$ dotgit init

    This command creates an empty filelist and also makes the first commit
    inside the repo. Next, we set up our filelist. We will set up the complete
    filelist now, since the ".xinitrc" file for the desktop won't be affected
    while we work on the laptop (since it is in a separate category). We edit
    the filelist to look as follows:

    # dotgit filelist
    .vimrc:laptop,desktop
    .xinitrc:laptop
    .xinitrc:desktop

    Our filelist is now ready. To update the dotgit repo to match it we run the
    update command inside the dotgit repo:

    [laptop]$ dotgit update -v

    Our repository now contains the newly-copied ".vimrc" file as well as the
    ".xinitrc" file for the laptop. To see these changes, we can run the diff
    command:

    [laptop]$ dotgit diff

    We are now done on the laptop, so we commit our changes to the repo and
    push it to the remote (something like GitHub):

    [laptop]$ dotgit commit

    Next, on the desktop we clone the repo to where we want to save it.
    Assuming that dotgit is already installed on the desktop we cd into the
    dotfiles repo. We first want to replace the ".vimrc" on the desktop with
    the one stored in the repo, so we run the restore command inside the repo:

    [desktop]$ dotgit restore -v

    Note that dotgit always replaces the file in the repo if the same file
    exists in your home folder and you run the "update" command. To prevent
    this from happening, run the restore command first in in the previous step.

    We now want to store the ".xinitrc" file from the desktop in our dotgit
    repo, so again we run the update operation.

    [desktop]$ dotgit update -v

    Again we save the changes to the dotfiles repo by committing it and pushing
    it to the remote:

    [desktop]$ dotgit commit

    Now we're done! To pull in the changes made from the desktop to the laptop,
    run "git pull" on the laptop. You might also need to run a "dotgit restore"
    on the laptop if you added new files to the filelist on the desktop.

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

    update         - Run this after you made changes to your filelist or if you
                     want to propagate changes from your home folder to your
                     repo if you are not using symlinks (e.g. encrypted files
                     or hard-copied files). This will update your dotgit repo's
                     structure to match your filelist, and copy any files from
                     the active categories to your dotgit repo as needed. Will
                     also remove files from the repo that is no longer in the
                     filelist.

    restore        - Transfers files from your dotgit repo to your home folder
                     (symlinking by default, but depends on the active plugin).
                     Use this to bootstrap a new machine after cloning your
                     dotfiles repo onto it. Running "update" automatically also
                     runs a "restore" operation.

    clean          - This will remove all the dotfiles managed by dotgit from
                     your home folder.

    diff           - This will print your current changes in your dotfiles
                     repository (does not show when there is unencrypted
                     changes)

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
