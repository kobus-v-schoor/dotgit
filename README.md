# dotgit

![tests](https://github.com/kobus-v-schoor/dotgit/workflows/tests/badge.svg)
[![coverage](https://coveralls.io/repos/github/kobus-v-schoor/dotgit/badge.svg?branch=python)](https://coveralls.io/github/kobus-v-schoor/dotgit?branch=python)
![publish](https://github.com/kobus-v-schoor/dotgit/workflows/publish/badge.svg)
[![downloads](https://img.shields.io/pypi/dm/dotgit)](https://pypi.org/project/dotgit/)

## A comprehensive and versatile dotfiles manager

dotgit will allows you to easily store all your dotfiles for any number of
machines in a single git repository. Written in python with no external
dependencies besides git, it works on both Linux and MacOS.

## Project goals

* Make it possible to store different versions of the same file in a single
  repository, but also to
* Make it possible to share the same file between more than one host/category
* Make use of an intuitive filelist
* Use simple one-liners to interact with dotgit
* Categorising of files
* Make using git with the repo easy without impairing git's power
* Keep all your dotfiles for different setups/machines in a single repository

## Why use dotgit?

* Easily keep several versions of the same file (e.g. for different hosts) in
  the same repo
* Easily share files between hosts (e.g. a common .vimrc)
* dotgit is managed through an intuitive filelist which allows you to easily
  set up complex configurations
* dotgit uses a straight-forward file-hierarchy similar to GNU Stow
* dotgit has an automated test suite that tests its functionality with several
  versions of Python on Linux and MacOS
* If you're uncomfortable with git, you can still easily use dotgit by letting
  dotgit work with git for you. If you prefer to work with git yourself you can
  easily do that - a dotgit repository is just a normal git repository and you
  don't need to use dotgit's git functionality at all if you don't want to.
* Support for both symlinking or copying dotfiles to your home directory.
  Copying allows you to quickly bootstrap a machine and remove the repo should
  you need to.
* No external dependencies apart from git

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
`server`. This makes it easy to keep separate configurations inside the same
repository.

## Installation

The easiest way to install dotgit is using pip:

```
pip install dotgit
```

Arch Linux users can also install the [AUR
package](https://aur.archlinux.org/packages/dotgit)

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
   filelist) with `dotgit update`. Once you do this your dotfile has been moved
   from your home directory to your dotfiles repo, and a symlink was created in
   your home directory in place of the original file pointing to the file
   inside your dotfiles repo.
6. Commit your changes to your dotgit repo by doing running `dotgit commit`

That's it! When you want to push your changes to your git remote you just do a
`git push` as usual (dotgit will also offer to do this for you).

If you change your dotfiles (e.g. you edit your `.bashrc` file) you don't need
to run an update operation again. You just cd into your dotfiles directory and
run `dotgit commit`. dotgit will generate a commit for you with a fitting
description and will offer to push your changes to your remote (should you have
one).

To restore your dotfiles on another machine, just clone your repo, install
dotgit and run `dotgit restore` inside your repo.

## Future goals

dotgit was written with a plugin architecture in mind. It currently only has
one plugin, namely the "plain" plugin, which just does symlinking. The
following plugins are planned for some future release:

* Encryption using GnuPG
* Templating

## Migrating from v1

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
  the logic that works very well for single files.

To make room for future improvements, the layout of the dotgit dotfiles repos
had to change. Unfortunately this means that the new repos are not directly
compatible with the old ones, although it is easy to migrate to the new
version's format. To do that, do the following:

* Insert steps here...

Should you decide you'd like to stick to the old version of dotgit, you are
welcome to do so. The link to the original script is _insert link here_.
Please note that I will not be able to support the old version anymore, and as
such your on your own if you decide to use the old version.
