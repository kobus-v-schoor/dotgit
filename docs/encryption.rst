==========
Encryption
==========

Using encryption dotgit allows you to encrypt files that you would rather not
be plaintext readable in your repo. This is achieved by encrypting the files
with GnuPG before storing them in your repo. You can specify that a file should
be encrypted by appending ``|encrypt`` to the filename in your filelist, for
example::

   .ssh/config|encrypt

When using encryption you need to take note of the following:

* Encrypted files are not directly linked to your dotfiles repository. This
  means you need to run ``dotgit update`` whenever you want to save changes you
  made to the files in your repo.
* Your encryption password is securely hashed and stored in your repository.
  While this hash is secure in theory (for implementation details see below)
  it's probably not a good idea to just leave this lying around in a public
  repo somewhere.

For those interested, the password is hashed using Python's hashlib library
using

* PKCS#5 function 2 key-derivation algorithm 
* 32-bits salt
* 100000 iterations of the SHA256 hash
