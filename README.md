# dotgit
## A simple bash program to store and manage all your dotfiles (multiple hosts) in a single git repo

Using dotgit will allow you to effortlessly store all your dotfiles in a single git repo. Dotgit doesn't only do storage - it also manages your dotfiles between multiple computers and devices.

## Project goals
* Make it possible to store different versions of the same file in a single repo, but also to
* Make it possible to share the same file between more than one host/category
* Make use of an intuitive filelist
* Use (easy) one-liners to set up repository on new host
* Categorise files
* Make usage with git convenient and easy, but don't impair git's power
* Keep ALL the dotfiles in one, single repository

## Why use dotgit?
* If you're uncomfortable with git, let dotgit work with git for you. But, if you prefer to work with git yourself you can easily do that - a dotgit repository is just a normal git repository, no frills
* Equally good support for both symlinks and copies
* No dependencies, just a bash script
* Intuitive filelist - easily create a complex repository storing all you're different configs
* Easily work with only a group of files in your repo (categories)
* Straightforward file-hierarchy

## What makes dotgit different?
While dotgit is one of many dotfile managers, there are some key differences when compared with others:
* [yadm](https://github.com/TheLocehiliosan/yadm) - dotgit's way of separating files for different hosts is a lot easier and doesn't involve renaming the files.
* [vcsh](https://github.com/RichiH/vcsh) - While vcsh is very powerful, dotgit is a lot easier to set up, use and maintain over multiple machines (the only time you run a dotgit command is when you changed the filelist). vcsh also uses multiple repositories, something I personally wanted to avoid when I tried versioning my dotfiles.
* [homeshick](https://github.com/andsens/homeshick) - dotgit also allows multiple configs (categories), but still keeps them in a single repository.

All the above tools are great, and I encourage you to check them out. Dotgit combines the features that I find lacking in the above tools, but this is only my 2 cents :)

## Usage example
Say you have a vimrc that you prefer to share between a laptop and a desktop (with the terribly original hostnames `laptop` and `desktop`) but you also have a Raspberry Pi where you prefer to keep another vimrc (with the hostname `pi`). There's also a .bashrc that you'd like to share between all three and a .foo file that you would like to have only on all of your servers. After initializing a folder with "dotgit init" you'd use this filelist:

```
.vimrc:desktop,laptop -- Will share the file between the two and keep them the same
.vimrc:pi -- Will be unique to the pi
.bashrc -- Will be shared between every device that shares this repo, regardless of hostname (unless a category is used)
.foo:server -- Will only be linked into the home folder if you use the category server
```
Simply running `dotgit update` in your dotgit repo would set up symlinking hierarchy (or copy files into repo) and link all the files into your home directory. Restoring all your symlinks (or copies) from the repository is just as simple. Run `dotgit restore` and all the files that are relevant to the host will be symlinked (ord copied) into your home folder.

If you'd like to see a dotgit repo in action you can look at my [dotfiles](https://github.com/Cube777/dotfiles)

## Installation
Arch Linux- [AUR Package](https://aur.archlinux.org/packages/dotgit)

A system-wide install is not necessary - you can simply run dotgit out of a local bin folder. If you don't have one set up you can run the following:
```
mkdir ~/.bin
curl -L https://github.com/Cube777/dotgit/raw/master/dotgit > ~/.bin/dotgit
curl -L https://github.com/Cube777/dotgit/raw/master/bash_completion >> ~/.bash_completion
echo 'export PATH="$PATH:$HOME/.bin"' >> ~/.bashrc
```

(Any help with packaging for a different distro will be appreciated)

## Instructions
Remember that this is simply a git repo so all the usual git tricks work perfectly :)
There are two way to start up a repo: First is to create your online repo, clone it and then run `dotgit init` (alias for `git init` and creating a file and folder needed for dotgit) in it or you can simply make an empty dir, run `dotgit init` inside of it and then `dotgit add-remote "repo url"`.

Now all you have to do is edit the filelist (help message explains syntax) to your needs and you will be ready to do `dotgit update` :) The help message will explain the other options available to you, and I would recommend reading it as it has quite a few important notes. If you have any problems or feature requests please inform me of them and I will be glad to help.
