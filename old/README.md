# dotgit
## A comprehensive and versatile dotfiles manager

Using dotgit will allow you to effortlessly store all your dotfiles in a single
git repository. dotgit doesn't only do storage - it also manages your dotfiles
between multiple computers and devices.

## Project goals
* Make it possible to store different versions of the same file in a single
  repository, but also to
* Make it possible to share the same file between more than one host/category
* Make use of an intuitive filelist
* Use (easy) one-liners to set up repository on new host
* Categorise files
* Make usage with git convenient and easy, but don't impair git's power
* Keep ALL the dotfiles in one, single repository
* Support for directories
* Support for encryption

## Why use dotgit?
* If you're uncomfortable with git, let dotgit work with git for you. If you
  prefer to work with git yourself you can easily do that - a dotgit repository
  is just a normal git repository, no frills
* Equally good support for both symlinks and copies
* No dependencies, just a bash script
* Intuitive filelist - easily create a complex repository storing all your
  different configurations
* Easily work with only a group of files in your repository (categories)
* Straightforward file-hierarchy
* Support for directories
* Secure implementation of GnuPG AES encryption

## What makes dotgit different?
While dotgit is one of many dotfile managers, there are some key differences
when compared with others:
* [yadm](https://github.com/TheLocehiliosan/yadm) - dotgit's way of separating
  files for different hosts is a lot easier and doesn't involve renaming the
  files.
* [vcsh](https://github.com/RichiH/vcsh) - While vcsh is very powerful, dotgit
  is a lot easier to set up, use and maintain over multiple machines (the only
  time you run a dotgit command is when you changed the filelist). vcsh also
  uses multiple repositories, something I personally wanted to avoid when I
  tried versioning my dotfiles.
* [homeshick](https://github.com/andsens/homeshick) - dotgit also allows
  multiple configurations (categories), but still keeps them in a single
  repository.

All the above tools are great, and I encourage you to check them out. dotgit
combines the features that I find lacking in the above tools, but this is only
my 2 cents :)

## Usage example
Consider the following example filelist:
```
.vimrc:desktop,laptop
.vimrc:pi
.bashrc
.foo:server
```

Firstly, there will be two .vimrc files. The first one will be shared between
the hosts `desktop` and `laptop`. They will both be kept exactly the same -
whenever you change it on the one host, you will get the changes on the other
(you will obviously first need to do a `git pull` inside the repository to get
the new changes from the online repository). There will also be a separate
`.vimrc` inside the dotgit repository that will only be used with the `pi` host.

Since no host was specified with `.bashrc` it will reside inside the `common`
folder. This means that it will be shared among all hosts using this dotgit
repository (unless a category is specifically used along with the dotgit
commands).

Lastly the `.foo` will only be used when you explicitly use the category
`server`. This makes it easy to keep separate configurations inside the same
repository.

If you'd like to see a dotgit repository in action you can look at my
[dotfiles](https://github.com/kobus-v-schoor/dotfiles-dotgit) where I keep the dotfiles
of 3 PC's that I regularly use.

## Installation
Arch Linux- [AUR Package](https://aur.archlinux.org/packages/dotgit)

A system-wide install is not necessary - you can simply run dotgit out of a
local bin folder. If you don't have one set up you can run the following:
```
git clone https://github.com/kobus-v-schoor/dotgit
mkdir -p ~/.bin
cp -r dotgit/bin/dotgit* ~/.bin
cat dotgit/bin/bash_completion >> ~/.bash_completion
rm -rf dotgit
echo 'export PATH="$PATH:$HOME/.bin"' >> ~/.bashrc
```

To install fish shell completion:
```
cp dotgit/bin/fish_completion.fish ~/.config/fish/completions/dotgit.fish
```

(Any help with packaging for a different distro will be appreciated)

## Instructions
Remember that this is simply a git repository so all the usual git tricks work
perfectly :)

Create your online git repository, clone it (`git clone {repo_url}`) and then
run `dotgit init` inside your repository (alias for `git init` and creating a
file and folder needed for dotgit)

Now all you have to do is edit the filelist (help message explains syntax) to
your needs and you will be ready to do `dotgit update` :) The help message will
explain the other options available to you, and I would recommend reading it as
it has quite a few important notes. If you have any problems or feature requests
please inform me of them and I will be glad to help.
