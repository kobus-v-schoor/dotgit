from dotgit.plugins.encrypt import GPG, hash_file, EncryptPlugin


class TestGPG:
    def setup_io(self, tmp_path):
        txt = 'hello world'

        input_file = (tmp_path / 'input')
        input_file.write_text(txt)

        output_file = (tmp_path / 'output')
        return txt, input_file, output_file

    def test_encrypt_decrypt(self, tmp_path):
        txt, input_file, output_file = self.setup_io(tmp_path)
        gpg = GPG(txt)

        # encrypt the file
        gpg.encrypt(str(input_file), str(output_file))
        assert output_file.read_bytes() != input_file.read_bytes()

        # decrypt the file
        input_file.unlink()
        assert not input_file.exists()
        gpg.decrypt(str(output_file), str(input_file))
        assert input_file.read_text() == txt

class TestHash:
    def test_hash(self, tmp_path):
        f = tmp_path / 'file'
        f.write_text('hello world')
        assert (hash_file(str(f)) == 'b94d27b9934d3e08a52e52d7da7dabfac484efe3'
                '7a5380ee9088f7ace2efcde9')


class TestEncryptPlugin:
    def test_setup(self, tmp_path):
        (tmp_path / 'hashes').write_text('{"foo": "abcde"}')
        plugin = EncryptPlugin(data_dir=str(tmp_path))

        assert plugin.hashes == {'foo': 'abcde'}

    def test_apply(self, tmp_path, monkeypatch):
        sfile = tmp_path / 'source'
        dfile = tmp_path / 'dest'
        tfile = tmp_path / 'temp'

        txt = 'hello world'
        sfile.write_text(txt)

        password = 'password123'
        monkeypatch.setattr('getpass.getpass', lambda prompt: password)

        plugin = EncryptPlugin(data_dir=str(tmp_path), repo_dir=str(tmp_path))
        plugin.apply(str(sfile), str(dfile))

        assert sfile.read_bytes() != dfile.read_bytes()

        gpg = GPG(password)
        gpg.decrypt(str(dfile), str(tfile))

        rel_path = str(dfile.relative_to(tmp_path))

        assert tfile.read_text() == txt
        assert rel_path in plugin.hashes
        assert plugin.hashes[rel_path] == hash_file(str(sfile))
        assert (tmp_path / "hashes").read_text()

    def test_remove(self, tmp_path, monkeypatch):
        txt = 'hello world'
        password = 'password123'

        tfile = tmp_path / 'temp'
        sfile = tmp_path / 'source'
        dfile = tmp_path / 'dest'

        tfile.write_text(txt)
        gpg = GPG(password)
        gpg.encrypt(str(tfile), str(sfile))

        monkeypatch.setattr('getpass.getpass', lambda prompt: password)
        plugin = EncryptPlugin(data_dir=str(tmp_path))

        plugin.remove(str(sfile), str(dfile))

        assert dfile.read_text() == tfile.read_text()

    def test_samefile(self, tmp_path, monkeypatch):
        txt = 'hello world'
        password = 'password123'

        sfile = tmp_path / 'source'
        dfile = tmp_path / 'dest'

        sfile.write_text(txt)

        monkeypatch.setattr('getpass.getpass', lambda prompt: password)
        plugin = EncryptPlugin(data_dir=str(tmp_path))

        plugin.apply(str(sfile), str(dfile))

        assert hash_file(str(sfile)) != hash_file(str(dfile))
        assert plugin.samefile(repo_file=str(dfile), ext_file=str(sfile))

    def test_verify(self, tmp_path, monkeypatch):
        txt = 'hello world'
        password = 'password123'

        sfile = tmp_path / 'source'
        dfile = tmp_path / 'dest'

        sfile.write_text(txt)

        monkeypatch.setattr('getpass.getpass', lambda prompt: password)
        plugin = EncryptPlugin(data_dir=str(tmp_path))
        # store password by encrypting one file
        plugin.apply(str(sfile), str(dfile))

        assert plugin.verify_password(password)
        assert not plugin.verify_password(password + '123')

    def test_change_password(self, tmp_path, monkeypatch):
        txt = 'hello world'
        password = 'password123'

        repo = tmp_path / 'repo'
        repo.mkdir()

        sfile = tmp_path / 'source'
        dfile = repo / 'dest'

        sfile.write_text(txt)

        monkeypatch.setattr('getpass.getpass', lambda prompt: password)
        plugin = EncryptPlugin(data_dir=str(tmp_path))

        plugin.apply(str(sfile), str(dfile))

        password = password + '123'
        plugin.change_password(repo=str(repo))
        gpg = GPG(password)

        tfile = tmp_path / 'temp'
        gpg.decrypt(str(dfile), str(tfile))

        assert tfile.read_text() == txt
