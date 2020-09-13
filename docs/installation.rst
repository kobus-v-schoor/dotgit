============
Installation
============

System package manager
======================

* Arch Linux: `AUR package <https://aur.archlinux.org/packages/dotgit>`_

Install using Pip
=================

The easiest method to install dotgit if your system package manager does not
have a package is using Pip. You can install dotgit by running the following::

   pip3 install dotgit

Shell completion
================

If you didn't install dotgit using the system package manager you can get shell
completion working by installing the relevant completion scripts for your
shell.

Bash::

   url="https://raw.githubusercontent.com/kobus-v-schoor/dotgit/master/pkg/completion/bash.sh"
   curl "$url" >> ~/.bash_completion

Fish shell::

   url="https://raw.githubusercontent.com/kobus-v-schoor/dotgit/master/pkg/completion/fish.fish"
   curl --create-dirs "$url" >> ~/.config/fish/completions/dotgit.fish


Any help for non-bash completion scripts would be much appreciated :)

Manual installation
===================

If you do not want to install dotgit with a package manager you can also just
add this repo as a git submodule to your dotfiles repo. That way you get dotgit
whenever you clone your dotfiles repo with no install necessary.  Note that if
you choose this route you will need to manually update dotgit to the newest
version if there is a new release. To set this up, cd into your dotfiles repo
and run the following::

   cd ~/.dotfiles
   git submodule add https://github.com/kobus-v-schoor/dotgit
   git commit -m "Added dotgit submodule"


Now, whenever you clone your dotfiles repo you will have to pass an additional
flag to git to tell it to also clone the dotgit repo::

   git clone --recurse-submodules https://github.com/dotfiles/repo ~/.dotfiles

If you want to update the dotgit repo to the latest version run the following
inside your dotfiles repo::

   git submodule update --remote dotgit

Finally, to run dotgit it is easiest to set up an alias like the following (you
might need to adjust the path as well as the ``python3`` command depending on
your setup). You can then also set up the bash completion in the same way as
mentioned in `Shell completion`_. This is an example entry of what you might
want to put in your ``.bashrc`` file to make an alias (you'll probably want to
update the path to match your dotfiles repo)::

   alias dotgit="python3 ~/.dotfiles/dotgit/dotgit/__main__.py"
