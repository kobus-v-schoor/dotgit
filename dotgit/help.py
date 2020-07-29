HELP = '''
INITIAL SETUP:
    Firstly create an online git repository (eg. on GitHub). Clone this
    repository to your home folder ('git clone {repo_url} {repo_dest}', check
    online for more details). Next, cd into the repository and run 'dotgit
    init'. Next, setup your dogit repository by editing the filelist as
    explained in the "filelist syntax" section

FILELIST SYNTAX:
    There is only one file inside your dotgit repository that you will be
    editing namely the filelist (file named "filelist" in the root directory of
    your dotfiles repo)

    The filelist uses '#' at the beginning of a line do denote a comment.
    Blank lines are ignored.

    The filelist uses the following syntax:

    file_name:category1,category2

    or simply:

    file_name

    "file_name" can contain spaces and can be any file or folder inside your
    home directory. Categories allows you to group files together to more
    easily manage them as one group.  If no category is specified it is
    implicitly added to the "common" category. When you specify multiple
    categories for a single file dotgit will link their files together and they
    will share the same file. You can also use categories to separate different
    versions of the same file. For example:

    .vimrc:c1,c2
    .vimrc:c3

    In this example categories c1 and c2 will share the same .vimrc and c3 will
    have its own version of .vimrc. Categories can be anything you want it to
    be but there are two approaches that tend to work well.

    The most straight-forward usage is to use your hostnames of your machines
    as the categories. This works kind-of okay but the second approach tends to
    work better.

    A better approach is to group dotfiles that work together all in one
    category, e.g. you might group your .xinitrc and your .Xresources into one
    "x" category. Then use the groups functionality (explained below) to group
    these categories into your hosts

    After creating multiple categories it might become tedious to specify them
    all on the command-line, this is where category groups come in. Category
    groups also works well to group package groups (as explained above) into
    hosts. You can specify a group with the following syntax:

    group1=category1,category2

    Then, instead of running 'dotgit update category1 category2' every time you
    can just run 'dotgit update group1'. Implicitly added categories (common
    and your hostname) can also be expanded, meaning that if you have a group
    name that matches your hostname it will be expanded for you and you can
    just run 'dotgit update'. Building on the methodology explained above, a
    configuration that works well can be set up like this:

    laptop=x,vim
    desktop=x

    .vimrc:vim
    .xinitrc:x
    .Xresources:x

    .bashrc

    In the above example, the filelist contains two groups both matching the
    host names that they will be used on. "laptop" will make use of both the x
    and the vim packages (categories) and as such all the files listed on the
    filelist will be restored. On the "desktop" machine we decide to not use
    the vim configuration files, and so only the "x" files and the ".bashrc"
    file is restored.

OPTIONS:

    usage: dotgit   [-h] [--verbose] [--dry-run] [--hard] {action}
                    [category [category ...]]

    If you don't add any categories after your action, two categories, "common"
    and your hostname will be implicitly added. When you add categories only
    the files that are in those categories will be taken into consideration.
    For instance, if you specify "c1" after "update" only files marked with the
    "c1" category will be updated.

    It is recommended that you run dotgit with verbose mode (-v) and --dry-run
    turned on whenever you perform an update operation to see what would happen
    should you run your chosen command.

    init           - setup a new dotgit repository inside the current directory

    update         - run this only after you changed your filelist. This will
                     update the repository structure to match your filelist. Do
                     not use this if you only modified your dotfiles, it is
                     unnecessary. If you run dotgit in symlink mode take note
                     that running update will delete the original file inside
                     your home folder and replace it with a link to the
                     repository.

    restore        - run this to create links from your home folder to your
                     repository. You need to run this whenever you want to
                     setup a new machine or if you made changes to the filelist
                     on another machine and you want the changes to be added to
                     the current machine. Take note that dotgit will first
                     remove old links to your dotfiles repository and then
                     create the new links. You will thus need to specify all
                     the categories that you want to restore in one run

    clean          - This will remove all links in your home folder that point
                     to your dotfiles repository

    diff           - This will print your current changes in your dotfiles
                     repository

    commit         - This will generate a git commit message and push to a
                     remote if it can find one

    The 'update', 'restore' and 'clean' actions have a 'hard' mode, activated
    by using the --hard flag. When in this mode dotgit will copy the files
    to/from the repository rather than symlinking it.  In the case of 'clean'
    it will also remove files (that match the files inside the repo) and not
    just symlinks. This can be useful if you want to for example clone the
    repository onto a machine, restore your dotfiles and then delete the
    repository again.
'''
