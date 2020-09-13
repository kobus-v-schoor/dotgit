===============
Filelist syntax
===============

Your filelist is where all the magic happens, and correctly using dotgit's
categories and groups will make your life (or at least your dotfile management)
a lot easier.

The basic syntax is as follows:

* Blank lines are ignored
* Files starting with ``#`` are ignored (comments)
* All other lines are treated as filenames or group definitions

Filenames
==========

All the non-group lines (the group lines are the ones with a ``=`` in them) are
files that you want to store in your dotfiles repo. The filenames

* is everything up to a ``:`` or ``|`` character (or new line if those aren't
  present)
* can contain spaces
* is relative to your home directory

Categories
==========

When you specify a filename you can specify one or more "categories" that it
should belong to. These categories act like tags and can be anything you want
to group your dotfiles by. If a filename does not have a category specified it
is automatically added to the ``common`` category. Categories are specified in
the following way::

   # no category, automatically added to the "common" category
   .bashrc
   # added to the "tools" category
   .tmux.conf:tools
   # added to the "tools" and "vim" category
   .vimrc:tools,vim

When more than one category is specified for a file the file is linked between
the categories. This means that changes to the file will affect both
categories. This is very useful if for example you want to share a file between
two hosts::

   .vimrc:laptop,desktop

You can also store separate versions of a file by storing the different
versions under different categories::

   .vimrc:laptop
   .vimrc:desktop

Groups
======

Groups allow you to group multiple categories which makes working with multiple
categories a lot easier. They are defined using the following syntax::

   group=category1,category2

Along with dotgit's automatic hostname category (see the :doc:`usage` section
for more details) groups become very useful. Have a look at the
:doc:`org_schemes` section for how this could be used.

Plugins
=======

Plugins allow you to go beyond dotgit's normal symlinking of dotfiles.
Currently dotgit only has one plugin named ``encrypt``, which allows you to
encrypt your dotfiles using GnuPG. Plugins are specified using the ``|``
character::

   # no categories with a plugin
   .ssh/config|encrypt
   # using categories with a plugin
   .ssh/config:laptop,desktop|encrypt

Only one plugin can be chosen at a time and if categories are specified they
must be specified before the plugin.

Putting it all together
=======================

An example filelist might look something like this::

   # grouping makes organization a breeze
   laptop=tools,x,ssh
   desktop=tools,x

   # sharing/splitting of dotfiles between hosts/categories
   .vimrc:tools,vim
   .vimrc:pi

   .xinitrc:x

   # encryption support using GnuPG
   .ssh/id_rsa:ssh|encrypt
   .ssh/id_rsa.pub:ssh|encrypt
   .gitconfig|encrypt

   .bashrc

   # easily group dotfiles to keep them separate but still in the same repo
   .foo:server
