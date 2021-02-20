===============
Getting started
===============

Setting up your first dotgit repo
=================================

Before starting you will need to choose a location to store your dotfiles. This
should be a separate folder from your home directory, for example
``~/.dotfiles``.  It is also assumed that you have already installed dotgit. If
not, head on over to the :doc:`installation` section first.

You will probably want to store your dotfiles on some online hosting platform
like GitHub. If so, firstly go and create a new repository on that platform.
Clone the repository to your chosen dotfiles location and ``cd`` into it::

   git clone https://github.com/username/dotfiles ~/.dotfiles
   cd ~/.dotfiles

From this point onward it is assumed that you are running all of the commands
while inside your dotgit repo. Whenever you want to set up a new dotgit repo
you first need to initialize it. To do that, run the ``init`` command::

   dotgit init -v

Running this will create your filelist (unsurprisingly in a file named
``filelist``) for you. Your filelist will contain all the dotfiles you want to
store inside your dotgit repo, as well as what plugins and categories you want
them to belong to (check out the :doc:`filelist` section for more info on
those). For now, we'll just add your bash config file to your repo. Note that
the path is relative to your home directory, and as such you only specify
``.bashrc`` and not its full path::

   echo .bashrc >> filelist

Now that you have made changes to your filelist you need to update your repo.
This will copy over your files to your dotgit repo and set up the links in your
home folder pointing to them. To do so, run the ``update`` command::

   dotgit update -v

The ``update`` command does two things. Firstly it copies your file from your
home directory into your dotfiles repo and then it creates a symlink in your
home folder that links to this file. Your dotfiles repo will now look something
like this::

   ~/.dotfiles
   ├── dotfiles
   │   └── plain
   │       └── common
   │           └── .bashrc
   └── filelist

And in your home folder you should see a symlink to your dotfiles repo::

   readlink ~/.bashrc
   /home/user/.dotfiles/dotfiles/plain/common/.bashrc

To commit your changes you can either do so by using git directly or making use
of dotgit's convenient ``commit`` command::

   dotgit commit -v

This will commit all your changes and also generate a meaningful commit
message, and if your repo has a remote it will also ask if it should push your
changes to it. Note that you never need to use dotgit's git capabilities, your
dotgit repo is just a plain git repo and the git commands are merely there for
convenience. If you want to go ahead and set up some crazy git hooks or make
use of branches and tags you are welcome to do so, dotgit won't get in your
way.

Example workflow for multiple hosts
===================================

In this example we will set up two machines to use dotgit. The first will be
named "laptop" and the second "desktop". We want to share a ".vimrc" file
between the two but have separate ".xinitrc" files. Note that this example
doesn't follow the recommended filelist structure as outlined in the
:doc:`cookbook`, but is merely set up as an example.

First we start on the laptop. On it we have the ".vimrc" file that we want to
share as well as the ".xinitrc" file for the laptop. We create a new dotgit
repo (cloning an empty repo or just making an empty directory) and initialize
the repo by running the ``init`` command inside the repo::

   [laptop]$ dotgit init

This command creates an empty filelist and also makes the first commit inside
the repo. Next, we set up our filelist. We will set up the complete filelist
now, since the ".xinitrc" file for the desktop won't be affected while we work
on the laptop (since it is in a separate category). We edit the filelist to
look as follows::

   # dotgit filelist
   .vimrc:laptop,desktop
   .xinitrc:laptop
   .xinitrc:desktop

Our filelist is now ready. To update the dotgit repo it we run the update
command inside the dotgit repo::

   [laptop]$ dotgit update -v

Our repository now contains the newly-copied ".vimrc" file as well as the
".xinitrc" file for the laptop. To see these changes, we can run the ``diff``
command::

   [laptop]$ dotgit diff

We are now done on the laptop, so we commit our changes to the repo and push it
to the remote (something like GitHub)::

   [laptop]$ dotgit commit

Next, on the desktop we clone the repo to where we want to save it. Assuming
that dotgit is already installed on the desktop we cd into the dotfiles repo.
We first want to replace the ".vimrc" on the desktop with the one stored in the
repo, so we run the ``restore`` command inside the repo::

   [desktop]$ dotgit restore -v

.. note::
   When you run the ``update`` command dotgit will replace any files in the
   repo with those in your home folder. This is why we first ran the
   ``restore`` command in the previous step, otherwise the ".vimrc" that might
   have already been present on the desktop would have replaced the one in the
   repo.

We now want to store the ".xinitrc" file from the desktop in our dotgit repo,
so again we run the update command::

   [desktop]$ dotgit update -v

We then save changes to the dotfiles repo by committing it and pushing it to
the remote::

   [desktop]$ dotgit commit

Now we're done! The repo now contains the ".vimrc" as well as the two
".xinitrc" files from the desktop and laptop. In the future, if you made
changes to your ".vimrc" file on your laptop you would commit and push it, and
then run ``git pull`` on the desktop to get the changes on the desktop as well.
