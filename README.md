# dotgit

![tests](https://github.com/kobus-v-schoor/dotgit/workflows/tests/badge.svg)
[![coverage](https://coveralls.io/repos/github/kobus-v-schoor/dotgit/badge.svg)](https://coveralls.io/github/kobus-v-schoor/dotgit)
![publish-pypi](https://github.com/kobus-v-schoor/dotgit/workflows/publish-pypi/badge.svg)
[![downloads](https://img.shields.io/pypi/dm/dotgit)](https://pypi.org/project/dotgit/)

## A comprehensive and versatile dotfiles manager

dotgit will allows you to easily store all your dotfiles for any number of
machines in a single git repository. Written in python with no external
dependencies besides git, it works on both Linux and MacOS (should also work on
other \*nix environments)

## Project goals

* Share files between machines or keep separate versions, all in the same repo
* Make use of an intuitive filelist
* Grouping of files to make organization easy
* Make git source-control convenient and easy to use

## Why use dotgit?

* You can very easily organize and categorize your dotfiles, making it easy to
  store different setups in the same repo (e.g. your workstation and your
  headless server dotfiles, both in the same repo)
* dotgit was designed with its most important goal being to make managing
  multiple machine's dotfiles easy, by allowing to easily share and separate
  dotfiles between machines
* Ease-of-use is baked into everything without hindering more advanced users.
  For instance, dotgit can automatically commit and push commits for you should
  you want it to, but you can just as easily make the commits yourself
* dotgit has an automated test suite that tests its functionality with several
  versions of Python on Linux and MacOS to ensure cross-platform compatibility
* Support for both symlinking or copying dotfiles to your home directory.
  Copying allows you to quickly bootstrap a machine without leaving your repo
  or dotgit on it
* No external dependencies apart from git allowing you to install and use
  dotgit easily in any environment that supports Python

## Usage example

An example filelist might look something like this:


```
laptop=tools,x
desktop=tools,x

.vimrc:tools
.vimrc:pi

.xinitrc:x

.bashrc

.foo:server
```

Firstly, there will be two .vimrc files. The first one will be shared between
the hosts `desktop` and `laptop`. There will also be a separate `.vimrc` inside
the dotgit repository that will only be used with the `pi` host.

The second thing to notice is that you can use categories to group dotfiles. In
the example there is a `tools` and `x` category. This makes working with a
group of dotfiles a breeze.

Since no host was specified with `.bashrc` it will reside inside the `common`
category. This means that it will be shared among all hosts using this dotgit
repository (unless a category is specifically used along with the dotgit
commands).

Lastly the `.foo` will only be used when you explicitly use the category
`server`. This way you can for instance keep your "server" dotfiles in your
main dotfiles repo without cluttering your normal dotgit workflow.

You can also have a look at my personal dotfiles which I manage with dotgit
[here](https://github.com/kobus-v-schoor/dotfiles).

## Installation

Arch Linux users can install the
[AUR package](https://aur.archlinux.org/packages/dotgit).

If you are not on Arch, the easiest way to install dotgit is using pip
(substitute `pip` with `pip3` if you're on a Debian-like system):

```
pip install dotgit
```

You can also get bash-completion to work by installing dotgit's bash-completion
in your home folder:

```
curl https://raw.githubusercontent.com/kobus-v-schoor/dotgit/master/pkg/completion/bash.sh >> ~/.bash_completion
```

## Getting started

1. Choose a folder where you want to store your dotfiles, `~/.dotfiles` is a
   good place to start
2. Create your dotfiles folder and `cd` to it `mkdir -p ~/.dotfiles; cd
   ~/.dotfiles`
3. Initialize your dotgit repo with `dotgit init`. You can also skip the first
   two steps and clone an empty repo that you created somewhere e.g. on Github
   and run the init step inside the cloned repo.
4. Add your first dotfile `echo .bashrc >> filelist`
5. Update your dotgit repo (you need to do this whenever you change the
   filelist) with `dotgit update -v`. Once you do this your dotfile has been
   moved from your home directory to your dotfiles repo, and a symlink was
   created in your home directory in place of the original file pointing to the
   file inside your dotfiles repo.
6. Commit your changes to your dotgit repo by running `dotgit commit`

That's it! When you want to push your changes to your git remote you just do a
`git push` as usual (dotgit will also offer to do this for you).

If you change your dotfiles (e.g. you edit your `.bashrc` file) you don't need
to run an update operation again. You just cd into your dotfiles directory and
run `dotgit commit`. dotgit will generate a commit for you with a fitting
description and will offer to push your changes to your remote (should you have
one).

To restore your dotfiles on another machine, just clone your repo, install
dotgit and run `dotgit restore` inside your repo.

It is strongly recommended to look through dotgit's help by running `dotgit
--help`. This will show you good ways to use dotgit and explain dotgit's options
in detail.

## Future goals

dotgit was written with a plugin architecture. It currently only has one plugin,
namely the "plain" plugin, which just does symlinking. The following plugins are
planned for future releases:

* Encryption using GnuPG
* Templating

## Migrating from v1.x

After many years dotgit was finally completely rewritten in python. The first
version was written in pure bash, and while this was appealing at first it
quickly became a nightmare from a maintenance point-of-view. The new python
rewrite comes with many advantages including:

* Much better cross-platform compatibility, especially for MacOS. Using
  utilities like `find` became problematic between different environments
* A fully automated test suite to test dotgit on both Linux and MacOS
* Code that the author can understand after not seeing it for a week
* Unified install method (pip) for all the platforms

Currently, two features are missing from the python rewrite:

* Encryption support: this will be added in a future release
* Directory support: after much consideration it was decided to rather to not
  re-implement this. It requires a lot of special treatment that breaks some of
  the logic that works very well for single files. Excluding it made the
  file-handling logic much more robust

Should you decide you'd like to stick to the old version of dotgit, you are
welcome to do so. Installing the pip package will also make the original dotgit
available as the command "dotgit.sh" (AUR package as well). Please note that I
will not be able to support the old version anymore, and as such you're on your
own if you decide to use the old version.

To make room for future improvements, the layout of the dotgit dotfiles repos
had to change. Unfortunately this means that the new repos are not directly
compatible with the old ones, although it is easy to migrate to the new
version's format. To do so, do the following:

- Firstly, backup your current dotfiles repo in case something goes wrong
- Next, inside your dotfiles repo, move the dotfiles folder to its new location
  by running `mv dotfiles tmp; mkdir dotfiles; mv tmp dotfiles/plain`.
- You can leave your filelist as-is, the filelist syntax hasn't changed. You
  will need to delete your "cryptlist" file as this signals to dotgit that this
  is an old repo. Once the new version supports encryption it will not make use
  of a separate "cryptlist" file anyway, so there is no reason to keep it. Note
  that the encrypted files in your repo will be deleted once you run the new
  dotgit since it won't be able to find them in the filelist.
- With the new version of dotgit, run `dotgit update -v`. This will update the
  repo if necessary and will also fix the symlinks in your home folder.
- Commit the changes to your repo using either git or `dotgit commit`
- Familiarize yourself with the new dotgit syntax which has changed slightly to
  better follow conventions commonly found on the command-line by reading
  through the help using `dotgit -h`
