import os

from dotgit.plugins.plain import PlainPlugin


class TestPlainPlugin:
    def test_apply(self, tmp_path):
        plugin = PlainPlugin(str(tmp_path / 'data'))

        data = 'test data'

        with open(tmp_path / 'file', 'w') as f:
            f.write(data)

        plugin.apply(tmp_path / 'file', tmp_path / 'file2')

        assert (tmp_path / 'file').exists()
        assert (tmp_path / 'file2').exists()
        assert not (tmp_path / 'file').is_symlink()
        assert not (tmp_path / 'file2').is_symlink()

        with open(tmp_path / 'file2', 'r') as f:
            assert f.read() == data

    def test_remove(self, tmp_path):
        plugin = PlainPlugin(str(tmp_path / 'data'))

        open(tmp_path / 'file', 'w').close()
        plugin.remove(tmp_path / 'file', tmp_path / 'file2')

        assert (tmp_path / 'file').exists()
        assert (tmp_path / 'file2').exists()
        assert not (tmp_path / 'file').is_symlink()
        assert (tmp_path / 'file2').is_symlink()
        assert (tmp_path / 'file').samefile(tmp_path / 'file2')

    def test_samefile_link(self, tmp_path):
        plugin = PlainPlugin(str(tmp_path / 'data'))

        open(tmp_path / 'file', 'w').close()
        os.symlink(tmp_path / 'file', tmp_path / 'file2')

        assert plugin.samefile(tmp_path / 'file', tmp_path / 'file2')

    def test_samefile_copy(self, tmp_path):
        plugin = PlainPlugin(str(tmp_path / 'data'))

        open(tmp_path / 'file', 'w').close()
        open(tmp_path / 'file2', 'w').close()

        assert not plugin.samefile(tmp_path / 'file', tmp_path / 'file2')

    def test_hard_mode(self, tmp_path):
        plugin = PlainPlugin(str(tmp_path / 'data'), hard=True)

        open(tmp_path / 'file', 'w').close()
        plugin.remove(tmp_path / 'file', tmp_path / 'file2')

        assert (tmp_path / 'file').exists()
        assert (tmp_path / 'file2').exists()
        assert not (tmp_path / 'file').is_symlink()
        assert not (tmp_path / 'file2').is_symlink()
        assert not (tmp_path / 'file').samefile(tmp_path / 'file2')
