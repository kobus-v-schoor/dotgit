# dotgit

![tests](https://github.com/kobus-v-schoor/dotgit/workflows/tests/badge.svg)
[![coverage](https://coveralls.io/repos/github/kobus-v-schoor/dotgit/badge.svg)](https://coveralls.io/github/kobus-v-schoor/dotgit)
![publish-pypi](https://github.com/kobus-v-schoor/dotgit/workflows/publish-pypi/badge.svg)
[![docs](https://readthedocs.org/projects/dotgit/badge/?version=latest)](https://dotgit.readthedocs.io/en/latest/)
[![downloads](https://img.shields.io/pypi/dm/dotgit)](https://pypi.org/project/dotgit/)

## A comprehensive and versatile dotfiles manager

dotgit allows you to easily store, organize and manage all your dotfiles for
any number of machines. Written in python with no external dependencies besides
git, it works on both Linux and MacOS (should also work on other \*nix
environments).

## Project goals

* Share files between machines or keep separate versions, all in the same repo
  without any funny shenanigans
* Make use of an intuitive filelist which makes organization easy
* Make git version control convenient and easy to use

## Why use dotgit?

* You can very easily organize and categorize your dotfiles, making it easy to
  store different setups in the same repo (e.g. your workstation and your
  headless server dotfiles, stored and managed together)
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
* Encryption using GnuPG supported to allow you to store sensitive dotfiles

## Getting started

To get started with dotgit have a look at dotgit's documentation at
[https://dotgit.readthedocs.io/](https://dotgit.readthedocs.io/).

## Future goals

The following features are on the wishlist for future releases (more
suggestions welcome):

* [x] Encryption using GnuPG
* [ ] Config file for default behaviour (e.g. verbosity level, hard mode)
* [ ] Templating

## Migration from v1.x

If you used the previous bash version of dotgit (pre-v2) you need to follow the
migration guide
[here](https://dotgit.readthedocs.io/en/latest/migration_v1.html) to make your
dotfiles repo compatible with the new version.

## Contributing

Contributions to dotgit are welcome, just open a PR here on the repo. Please
note that your contributions should be linted with Flake8 (you can check for
linting errors locally by running `make lint` in the repo) and should also be
covered using unit tests using the pytest framework.
