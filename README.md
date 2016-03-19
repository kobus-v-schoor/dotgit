# dotgit
## A simple bash program to backup and manage all your dotfiles (read multiple hosts) in a single git repo

Using this program will allow you to effortlessly backup and store all your dotfiles in a single git repo. Dotgit doesn't only do backups - it also manages your dotfiles between multiple computers and devices. It has the ability to keep multiple versions of the same file (example different vimrcs) in the same repo, but it also allows you to easily share the same file between two or more devices (like a bashrc). It also incorporates an easy-to-use category system, so you can group a bunch of dotfiles together and keep them in-sync and safe.

This makes the following situation possible:

Say you have a vimrc that you prefer to share between a laptop and a desktop (with the terribly original hostnames `laptop` and `desktop`) but you also have a Raspberry Pi where you prefer to keep another vimrc (with the hostname `pi`). You also have a .bashrc that you'd like to share between all three. You also have a .foo file that you would like to have only on all your servers. After initializing a folder with "dotgit init" you could edit the filelist too look like this:

```
.vimrc:desktop,laptop -- Will share the file between the two and keep them in-sync
.vimrc:pi -- Will be unique to the pi
.bashrc -- Will be shared between every device that shares this repo, regardless of hostname (unless a category is used)
.foo:server -- Will only be restored (copied to the home folder) if you use the category server
```
Simply running `dotgit update` in your dotgit repo would update the relevant files in the repo depending on what host you are running it on! Or if you fancy updating all your files in the server category you'd simply `dotgit update server`. Restoring the files you need (or updating the files in your home folder after changing it on another machine) is just as simple. Run `dotgit restore` and all the files that are relevant to the host will be copied over to your home folder.

Dotgit also:
* Can generate commit messages
* Can automatically push the repo to a remote
* Supports files that reside in folders (like .scripts/backup.sh)
* Supports spaces in filnames \0/
* Print a help message (awesome feature :P)

Its written in bash so its easy to set up and use :) If you have any questions or feature requests please feel free to request them!
