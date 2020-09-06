import subprocess
import shlex
import logging
import json
import getpass
import hashlib
import os

from dotgit.plugin import Plugin


class GPG:
    def __init__(self, password):
        self.password = password

    def run(self, cmd):
        if not type(cmd) is list:
            cmd = shlex.split(cmd)

        # these are needed to read the password from stdin
        pre = ['--passphrase-fd', '0', '--pinentry-mode', 'loopback']
        # insert pre into the gpg command string
        cmd = cmd[:1] + pre + cmd[1:]

        logging.debug(f'running gpg command {cmd}')

        try:
            proc = subprocess.run(cmd, input=self.password.encode(),
                                  stdout=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(e.stdout.decode())
            logging.error(f'gpg command {cmd} failed with exit code '
                          f'{e.returncode}\n')
            raise

        logging.debug(f'gpg command {cmd} succeeded')
        return proc.stdout.decode()

    def encrypt(self, input_file, output_file):
        self.run(f'gpg --armor --output {shlex.quote(output_file)} '
                 f'--symmetric {shlex.quote(input_file)}')

    def decrypt(self, input_file, output_file):
        self.run(f'gpg --output {shlex.quote(output_file)} '
                 f'--decrypt {shlex.quote(input_file)}')


# calculates the sha256 hash of the file at fpath
def hash_file(path):
    h = hashlib.sha256()

    with open(path, 'rb') as f:
        while True:
            chunk = f.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()


class EncryptPlugin(Plugin):
    def __init__(self, data_dir, *args, **kwargs):
        self.gpg = None
        self.hashes_path = os.path.join(data_dir, 'hashes')
        super().__init__(*args, data_dir=data_dir, **kwargs)

    # reads the stored hashes
    def setup_data(self):
        if os.path.exists(self.hashes_path):
            with open(self.hashes_path, 'r') as f:
                self.hashes = json.load(f)
        else:
            self.hashes = {}

    # saves the current hashes to the data dir
    def save_data(self):
        with open(self.hashes_path, 'w') as f:
            json.dump(self.hashes, f)

    # gets the password from the user if needed
    # TODO check if password is correct
    def init_password(self):
        if self.gpg is not None:
            return

        password = getpass.getpass(prompt='Encryption password: ')
        self.gpg = GPG(password)

    # encrypts a file from outside the repo and stores it inside the repo
    def apply(self, source, dest):
        self.init_password()
        self.gpg.encrypt(source, dest)

        # calculate and store file hash
        self.hashes[dest] = hash_file(source)
        self.save_data()

    # decrypts source and saves it in dest
    def remove(self, source, dest):
        self.init_password()
        self.gpg.decrypt(source, dest)

    # compares the ext_file to repo_file and returns true if they are the same.
    # does this by looking at the repo_file's hash and calculating the hash of
    # the ext_file
    def samefile(self, repo_file, ext_file):
        ext_hash = hash_file(ext_file)
        return self.hashes[repo_file] == ext_hash

    def strify(self, op):
        if op == self.apply:
            return "ENCRYPT"
        elif op == self.remove:
            return "DECRYPT"
        else:
            return ""
