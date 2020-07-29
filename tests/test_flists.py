import os
import pytest

from dotgit.flists import Filelist

class TestFilelist:
    def write_flist(self, tmp_path, content):
        fname = os.path.join(tmp_path, 'filelist')
        with open(fname, 'w') as f:
            f.write(content)
        return fname

    def test_comments_and_empty(self, tmp_path):
        fname = self.write_flist(tmp_path, '# test comment\n    '+
                '\n  # spaced comment\n')

        flist = Filelist(fname)
        assert flist.groups == {}
        assert flist.files == {}

    def test_group(self, tmp_path):
        fname = self.write_flist(tmp_path, 'group=cat1,cat2,cat3')

        flist = Filelist(fname)
        assert flist.groups == {'group': ['cat1', 'cat2', 'cat3']}
        assert flist.files == {}

    def test_common_file(self, tmp_path):
        fname = self.write_flist(tmp_path, 'common_file/with/path')

        flist = Filelist(fname)
        assert flist.groups == {}
        assert flist.files == {'common_file/with/path': [{
            'categories': ['common'],
            'plugin': 'plain'
        }]}

    def test_file(self, tmp_path):
        fname = self.write_flist(tmp_path, 'file:cat1,cat2\nfile:cat3\n')

        flist = Filelist(fname)
        assert flist.groups == {}
        assert flist.files == {
            'file': [{
                'categories': ['cat1', 'cat2'],
                'plugin': 'plain'
            }, {
                'categories': ['cat3'],
                'plugin': 'plain'
            }]}

    def test_mix(self, tmp_path):
        fname = self.write_flist(tmp_path,
                'group=cat1,cat2\ncfile\n#comment\nnfile:cat1,cat2\n')

        flist = Filelist(fname)
        assert flist.groups == {'group': ['cat1', 'cat2']}
        assert flist.files == {
            'cfile': [{
                'categories': ['common'],
                'plugin': 'plain'
            }],
            'nfile': [{
                'categories': ['cat1', 'cat2'],
                'plugin': 'plain'
            }]}

    def test_plugin(self, tmp_path):
        fname = self.write_flist(tmp_path, 'file:cat1,cat2:encrypt')

        flist = Filelist(fname)
        assert flist.files == {
            'file': [{
                'categories': ['cat1', 'cat2'],
                'plugin': 'encrypt'
            }]}

    def test_activate_groups(self, tmp_path):
        fname = self.write_flist(tmp_path, 'group=cat1,cat2\nfile:cat1')

        flist = Filelist(fname)
        assert flist.activate(['group']) == {
            'file': {
                'categories': ['cat1'],
                'plugin': 'plain'
            }}

    def test_activate_normal(self, tmp_path):
        fname = self.write_flist(tmp_path, 'file:cat1,cat2\nfile2:cat3\n')

        flist = Filelist(fname)
        assert flist.activate(['cat2']) == {
            'file': {
                'categories': ['cat1', 'cat2'],
                'plugin': 'plain',
            }}

    def test_activate_duplicate(self, tmp_path):
        fname = self.write_flist(tmp_path, 'file:cat1,cat2\nfile:cat2\n')

        flist = Filelist(fname)
        with pytest.raises(RuntimeError):
            flist.activate(['cat2'])

    def test_manifest(self, tmp_path):
        fname = self.write_flist(tmp_path,
                                 'group=cat1,cat2\ncfile\nnfile:cat1,cat2\n'
                                 'gfile:group\npfile:cat1,cat2:encrypt')

        flist = Filelist(fname)
        manifest = flist.manifest()

        assert type(manifest) is dict
        assert sorted(manifest) == sorted(['plain', 'encrypt'])

        assert sorted(manifest['plain']) == sorted(['common/cfile',
                                                    'cat1/nfile', 'cat2/nfile',
                                                    'cat1/gfile',
                                                    'cat2/gfile'])

        assert sorted(manifest['encrypt']) == sorted(['cat1/pfile',
                                                      'cat2/pfile'])
