from dotgit.plugins.encrypt import GPG, EncryptPlugin


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


class TestEncryptPlugin:
    pass
