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

Most importantly, running this will create your filelist (unsurprisingly in a
file named ``filelist``) for you. Your filelist will contain all the dotfiles
you want to store inside your dotgit repo, as well as what plugins and
categories you want them to belong to (more on that later). For now, we'll just
add your bash config file to your repo. Note that the path is relative to your
home directory, and as such you only specify ``.basrc`` and not its full path::

   echo .bashrc >> ~/filelist

Now that you have made changes to your filelist you need to update your repo.
This will copy over your files to your dotgit repo and set up the links in your
home folder pointing to them. To do so, run the ``update`` command::

   dotgit update -v

If you now check in your home folder, you will see that ``.bashrc`` is now a
symlink that points to your dotfiles repo. To commit your changes you can
either do so by using git directly or making use of dotgit's convenient
``commit`` command::

   dotgit commit -v

This will commit all your changes and also generate a meaningful commit
message, and if your repo has a remote it will also ask if it should push your
changes to it. Note that you never need to use dotgit's git capabilities, your
dotgit repo is just a plain git repo and the git commands are merely there for
convenience. If you want to go ahead and set up some crazy git hooks or make
use of branches and tags you are welcome to do so, dotgit won't get in your
way.
