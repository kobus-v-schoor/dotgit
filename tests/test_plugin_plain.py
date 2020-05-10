import os

from dotgit.plugin_plain import PlainPlugin


class TestPlainPlugin:
    def setup_pre_post_data(self, tmp_path):
        os.makedirs(tmp_path / 'pre')
        os.makedirs(tmp_path / 'post')
        os.makedirs(tmp_path / 'data')
        return tmp_path / 'pre', tmp_path / 'post', tmp_path / 'data'

    def test_init(self, tmp_path):
        pre, post, data = self.setup_pre_post_data(tmp_path)
        plugin = PlainPlugin(str(pre), str(post), str(data))

        assert plugin.pre_dir == str(pre)
        assert plugin.post_dir == str(post)
        assert plugin.data_dir == str(data)

    def test_apply(self, tmp_path):
        pre, post, data = self.setup_pre_post_data(tmp_path)
        plugin = PlainPlugin(str(pre), str(post), str(data))

        open(pre / 'file', 'w').close()
        plugin.apply('file')
        assert not (pre / 'file').is_symlink()
        assert (post / 'file').is_symlink()
        assert (pre / 'file').samefile(post / 'file')

    def test_remove(self, tmp_path):
        pre, post, data = self.setup_pre_post_data(tmp_path)
        plugin = PlainPlugin(str(pre), str(post), str(data))

        open(post / 'file', 'w').close()
        plugin.remove('file')
        assert not (pre / 'file').is_symlink()
        assert (post / 'file').is_symlink()
        assert (pre / 'file').samefile(post / 'file')
