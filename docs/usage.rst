=====
Usage
=====

The basic usage syntax for dotgit is the following::

   dotgit [flags] {action} [category [category]]

Where ``action`` is one of the actions listed below and ``category`` is one or
more categories or groups to activate. If no categories are specified dotgit
will automatically activate the ``common`` category as well as a category with
your machine's hostname.

Using categories
================

When you run dotgit all of its actions will be limited to the categories that
are activated. If you don't specify any categories the default behaviour is to
activate the ``common`` category as well as a category with your machine's
hostname (e.g. ``my-laptop``).

When a category is active and you run dotgit all the other files on the
filelist that are not in the specified category is ignored.

Flags
=====

.. option:: -h, --help

   Display a help message

.. option:: -v, --verbose

   Increase dotgit's verbosity level. Can be specified multiple times

.. option:: --dry-run

   When specified dotgit won't make any changes to the filesystem. Useful when
   running with ``-v`` to see what dotgit would do if you run a command

.. option:: --hard

   Activates "hard" mode where files are copied rather than symlinked. See the
   actions section for actions where this is used. Useful if symlinking isn't
   an option or if you want the dotfiles to live on the machine independently
   of the dotgit repo.

Actions
=======

.. option:: update

   Updates the dotgit repository. Run this after you made changes to your
   filelist or if you want to add the changes to non-symlinked files to your
   repo (e.g. encrypted files). This will save your dotfiles from your home
   folder in your dotgit repo, and also set up the links/copies to your
   dotfiles repo as needed (runs a ``restore`` operation after updating).

.. option:: restore

   Links or copies files from your dotgit repo to your home folder. Use this if
   you want to restore your dotfiles to a new machine.

.. option:: clean

   Removes all the dotfiles managed by dotgit from your home folder (run first
   with the ``-v --dry-run`` flags to see what dotgit plans on doing).

.. option:: diff

   Prints the current changes in your dotgit repo.

.. option:: commit

   This will generate a git commit with all the current changes in the repo and
   will ask you if you want to push the commit to a remote (if one is
   configured).
