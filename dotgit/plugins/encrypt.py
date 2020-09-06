import subprocess
import shlex
import logging

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


class EncryptPlugin(Plugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup_data(self):
        pass

    # encrypts a file from outside the repo and stores it inside the repo
    def apply(self, source, dest):
        pass

    # decrypts source and saves it in dest
    def remove(self, source, dest):
        pass

    # compares the ext_file to repo_file and returns true if they are the same.
    # does this by looking at the repo_file's hash and calculating the hash of
    # the ext_file
    def samefile(self, repo_file, ext_file):
        pass

    def strify(self, op):
        if op == self.apply:
            return "ENCRYPT"
        elif op == self.remove:
            return "DECRYPT"
        else:
            return ""
