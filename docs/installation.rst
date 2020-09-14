============
Installation
============

System package manager
======================

* Arch Linux: `AUR package <https://aur.archlinux.org/packages/dotgit>`_

Install using pip
=================

The easiest method to install dotgit is using pip (you might need to change the
command to ``pip3`` depending on your system)::

   pip install -U dotgit

If you are installing dotgit using pip make sure to check out the `Shell
completion`_ section to get tab-completion working.

Shell completion
================

If you did not install dotgit using the system package manager you can get
shell completion (tab-completion) working by installing the relevant dotgit
completion scripts for your shell.

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
version if there is a new release by pulling in the newest changes into your
repo. To set this up, cd into your dotfiles repo and run the following::

   cd ~/.dotfiles
   git submodule add https://github.com/kobus-v-schoor/dotgit
   git commit -m "Added dotgit submodule"


Now, whenever you clone your dotfiles repo you will have to pass an additional
flag to git to tell it to also clone the dotgit repo::

   git clone --recurse-submodules https://github.com/dotfiles/repo ~/.dotfiles

If you want to update the dotgit repo to the latest version run the following
inside your dotfiles repo::

   git submodule update --remote dotgit
   git commit -m "Updated dotgit"

Finally, to run dotgit it is easiest to set up something like an alias. You can
then also set up the bash completion in the same way as mentioned in `Shell
completion`_. This is an example entry of what you might want to put in your
``.bashrc`` file to make an alias (you'll probably want to update the path and
``python3`` command to match your setup)::

   alias dotgit="python3 ~/.dotfiles/dotgit/dotgit/__main__.py"
