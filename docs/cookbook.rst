========
Cookbook
========

This cookbook presents an approach to manage your filelist in such a way to
make your dotfiles management convenient and well-organized. There is obviously
many other ways to manage your filelist but this is my personal favourite as it
makes it easy to add or remove a group of dotfiles for a host and it still
provides a lot of flexibility.

The main idea is to define groups that match your hostnames and choose
categories that groups similar dotfiles (for example a "vim" or "tmux"
category).

An example filelist that follows this approach would look something like this::

   # group names matches the hosts you manage
   laptop=vim,tmux,x,tools
   desktop=vim,tmux,x

   # vim category
   .vimrc:vim

   # tmux category
   .tmux.conf:tmux

   # x category
   .xinitrc:x
   .Xresources:x

   # tools category
   .bin/hack_nsa.sh:tools
   .bin/change_btc_price.sh:tools

   # these files are managed manually per-host
   .inputrc:laptop
   .inputrc:desktop

This way you can easily add or remove a group of dotfiles for a host by simply
editing their group. And since the group name matches your hostname you don't
need to manually specify any categories when running dotgit commands (have a
look at the :doc:`usage` section to see why).
