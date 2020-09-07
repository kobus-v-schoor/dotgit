import subprocess
import shlex
import logging
import json
import getpass
import hashlib
import os
import tempfile

from dotgit.plugin import Plugin


class GPG:
    def __init__(self, password):
        self.password = password

    def run(self, cmd):
        if not type(cmd) is list:
            cmd = shlex.split(cmd)

        # these are needed to read the password from stdin and to not ask
        # questions
        pre = ['--passphrase-fd', '0', '--pinentry-mode', 'loopback',
               '--batch', '--yes']
        # insert pre into the gpg command string
        cmd = cmd[:1] + pre + cmd[1:]

        logging.debug(f'running gpg command {cmd}')

        try:
            proc = subprocess.run(cmd, input=self.password.encode(),
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(e.stderr.decode())
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


# hash password using suitable key-stretching algorithm
# salt needs to be >16 bits from a suitable cryptographically secure random
# source, but can be stored in plaintext
def key_stretch(password, salt):
    if type(password) is not bytes:
        password = password.encode()
    if type(salt) is not bytes:
        salt = bytes.fromhex(salt)
    key = hashlib.pbkdf2_hmac(hash_name='sha256', password=password, salt=salt,
                              iterations=100000)
    return key.hex()


class EncryptPlugin(Plugin):
    def __init__(self, data_dir, *args, **kwargs):
        self.gpg = None
        self.hashes_path = os.path.join(data_dir, 'hashes')
        self.modes_path = os.path.join(data_dir, 'modes')
        self.pword_path = os.path.join(data_dir, 'passwd')
        super().__init__(*args, data_dir=data_dir, **kwargs)

    # reads the stored hashes
    def setup_data(self):
        if os.path.exists(self.hashes_path):
            with open(self.hashes_path, 'r') as f:
                self.hashes = json.load(f)
        else:
            self.hashes = {}

        if os.path.exists(self.modes_path):
            with open(self.modes_path, 'r') as f:
                self.modes = json.load(f)
        else:
            self.modes = {}

    # removes file entries in modes and hashes that are no longer in the
    # manifest
    def clean_data(self, manifest):
        for data in [self.hashes, self.modes]:
            diff = set(data) - set(manifest)
            for key in diff:
                data.pop(key)
        self.save_data()

    # saves the current hashes and modes to the data dir
    def save_data(self):
        with open(self.hashes_path, 'w') as f:
            json.dump(self.hashes, f)
        with open(self.modes_path, 'w') as f:
            json.dump(self.modes, f)

    # sets the password in the plugin's data dir. do not use directly, use
    # change_password instead
    def save_password(self, password):
        # get salt from crypto-safe random source
        salt = os.urandom(32)
        # calculate password hash
        key = key_stretch(password.encode(), salt)

        # save salt and hash
        with open(self.pword_path, 'w') as f:
            d = {'pword': key, 'salt': salt.hex()}
            json.dump(d, f)

    # takes a password and checks if the correct password was entered
    def verify_password(self, password):
        with open(self.pword_path, 'r') as f:
            d = json.load(f)
        return key_stretch(password, d['salt']) == d['pword']

    # asks the user for a new password and re-encrypts all the files with the
    # new password. if repo is None no attempt is made to re-encrypt files
    def change_password(self, repo=None):
        while True:
            p1 = getpass.getpass(prompt='Enter new password: ')
            p2 = getpass.getpass(prompt='Re-enter new password: ')

            if p1 != p2:
                print('Entered passwords do not match, please try again')
            else:
                break

        new_pword = p1
        new_gpg = GPG(new_pword)

        if repo is not None:
            self.init_password()

            for root, dirs, files in os.walk(repo):
                for fname in files:
                    fname = os.path.join(root, fname)
                    logging.info(f'changing passphrase for '
                                 f'{os.path.relpath(fname, repo)}')

                    # make a secure temporary file
                    fs, sfname = tempfile.mkstemp()
                    # close the file-handle since we won't be using it (just
                    # there for gpg to write to)
                    os.close(fs)

                    try:
                        # decrypt with old passphrase and re-encrypt with new
                        # passphrase
                        self.gpg.decrypt(fname, sfname)
                        new_gpg.encrypt(sfname, fname)
                    except:  # noqa: E722
                        raise
                    finally:
                        os.remove(sfname)

        self.gpg = new_gpg
        self.save_password(new_pword)
        return new_pword

    # gets the password from the user if needed
    def init_password(self):
        if self.gpg is not None:
            return

        if not os.path.exists(self.pword_path):
            print('No encryption password was found for this repo. To '
                  'continue please set an encryption password\n')
            password = self.change_password()
        else:
            while True:
                password = getpass.getpass(prompt='Encryption password: ')
                if self.verify_password(password):
                    break
                print('Incorrect password entered, please try again')

        self.gpg = GPG(password)

    # encrypts a file from outside the repo and stores it inside the repo
    def apply(self, source, dest):
        self.init_password()
        self.gpg.encrypt(source, dest)

        # calculate and store file hash
        self.hashes[self.strip_repo(dest)] = hash_file(source)
        # store file mode data (metadata)
        self.modes[self.strip_repo(dest)] = os.stat(source).st_mode & 0o777

        self.save_data()

    # decrypts source and saves it in dest
    def remove(self, source, dest):
        self.init_password()
        self.gpg.decrypt(source, dest)
        os.chmod(dest, self.modes[self.strip_repo(source)])

    # compares the ext_file to repo_file and returns true if they are the same.
    # does this by looking at the repo_file's hash and calculating the hash of
    # the ext_file
    def samefile(self, repo_file, ext_file):
        ext_hash = hash_file(ext_file)
        repo_file = self.strip_repo(repo_file)
        return self.hashes.get(repo_file, None) == ext_hash

    def strify(self, op):
        if op == self.apply:
            return "ENCRYPT"
        elif op == self.remove:
            return "DECRYPT"
        else:
            return ""
