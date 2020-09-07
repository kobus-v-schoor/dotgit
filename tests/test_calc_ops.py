import os
from pathlib import Path

from dotgit.calc_ops import CalcOps
from dotgit.file_ops import FileOps
from dotgit.plugins.plain import PlainPlugin

class TestCalcOps:
    def setup_home_repo(self, tmp_path):
        os.makedirs(tmp_path / 'home')
        os.makedirs(tmp_path / 'repo')
        return tmp_path/'home', tmp_path/'repo'

    def test_update_no_cands(self, tmp_path, caplog):
        home, repo = self.setup_home_repo(tmp_path)
        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.update({'file': ['cat1', 'cat2']})
        assert 'unable to find any candidates' in caplog.text

    def test_update_master_noslave(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1')
        open(repo / 'cat1' / 'file', 'w').close()

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.update({'file': ['cat1', 'cat2']}).apply()

        assert (repo / 'cat1').is_dir()
        assert not (repo / 'cat1' / 'file').is_symlink()
        assert (repo / 'cat2').is_dir()
        assert (repo / 'cat2' / 'file').is_symlink()
        assert (repo / 'cat2' / 'file').samefile(repo / 'cat1' / 'file')

    def test_update_nomaster_slave(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat2')
        open(repo / 'cat2' / 'file', 'w').close()

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.update({'file': ['cat1', 'cat2']}).apply()

        assert (repo / 'cat1').is_dir()
        assert not (repo / 'cat1' / 'file').is_symlink()
        assert (repo / 'cat2').is_dir()
        assert (repo / 'cat2' / 'file').is_symlink()
        assert (repo / 'cat2' / 'file').samefile(repo / 'cat1' / 'file')

    def test_update_master_linkedslave(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1')
        os.makedirs(repo / 'cat2')
        open(repo / 'cat1' / 'file', 'w').close()
        os.symlink(Path('..') / 'cat1' / 'file', repo / 'cat2' / 'file')

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        assert calc.update({'file': ['cat1', 'cat2']}).ops == []

    def test_update_master_brokenlinkslave(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1')
        os.makedirs(repo / 'cat2')
        open(repo / 'cat1' / 'file', 'w').close()
        os.symlink(Path('..') / 'cat1' / 'nonexistent', repo / 'cat2' / 'file')

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.update({'file': ['cat1', 'cat2']}).apply()

        assert (repo / 'cat1').is_dir()
        assert not (repo / 'cat1' / 'file').is_symlink()
        assert (repo / 'cat2').is_dir()
        assert (repo / 'cat2' / 'file').is_symlink()
        assert (repo / 'cat2' / 'file').samefile(repo / 'cat1' / 'file')

    def test_update_home_nomaster_noslave(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        open(home / 'file', 'w').close()

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.update({'file': ['cat1', 'cat2']}).apply()

        assert (repo / 'cat1').is_dir()
        assert not (repo / 'cat1' / 'file').is_symlink()
        assert (repo / 'cat2').is_dir()
        assert (repo / 'cat2' / 'file').is_symlink()
        assert (repo / 'cat2' / 'file').samefile(repo / 'cat1' / 'file')
        assert not (home / 'file').exists()

    def test_update_linkedhome_master_noslave(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1')
        open(repo / 'cat1' / 'file', 'w').close()
        os.symlink(repo / 'cat1' / 'file', home / 'file')

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.update({'file': ['cat1', 'cat2']}).apply()

        assert (repo / 'cat1').is_dir()
        assert not (repo / 'cat1' / 'file').is_symlink()
        assert (repo / 'cat2').is_dir()
        assert (repo / 'cat2' / 'file').is_symlink()
        assert (repo / 'cat2' / 'file').samefile(repo / 'cat1' / 'file')
        assert (home / 'file').is_symlink()
        assert (home / 'file').samefile(repo / 'cat1' / 'file')

    def test_update_externallinkedhome_nomaster_noslave(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)

        (home / 'foo').touch()
        (home / 'file').symlink_to(home / 'foo')

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.update({'file': ['cat']}).apply()

        assert (repo / 'cat').is_dir()
        assert (repo / 'cat' / 'file').exists()
        assert not (repo / 'cat' / 'file').is_symlink()

        calc.restore({'file': ['cat']}).apply()

        assert (home / 'file').is_symlink()
        assert (home / 'file').samefile(repo / 'cat' / 'file')
        assert repo in (home / 'file').resolve().parents
        assert (home / 'foo').exists()
        assert not (home / 'foo').is_symlink()

    def test_update_changed_master(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat2')
        os.makedirs(repo / 'cat3')
        open(repo / 'cat2' / 'file', 'w').close()
        os.symlink(Path('..') / 'cat2' / 'file', repo / 'cat3' / 'file')

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.update({'file': ['cat1', 'cat2', 'cat3']}).apply()

        assert (repo / 'cat1').is_dir()
        assert not (repo / 'cat1' / 'file').is_symlink()
        assert (repo / 'cat2').is_dir()
        assert (repo / 'cat2' / 'file').is_symlink()
        assert (repo / 'cat2' / 'file').samefile(repo / 'cat1' / 'file')
        assert (repo / 'cat3').is_dir()
        assert (repo / 'cat3' / 'file').is_symlink()
        assert (repo / 'cat3' / 'file').samefile(repo / 'cat1' / 'file')

    def test_update_multiple_candidates(self, tmp_path, monkeypatch):
        home, repo = self.setup_home_repo(tmp_path)

        (repo / 'cat1').mkdir()
        (repo / 'cat2').mkdir()

        (repo / 'cat1' / 'file').write_text('file1')
        (repo / 'cat2' / 'file').write_text('file2')

        monkeypatch.setattr('builtins.input', lambda p: '1')

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.update({'file': ['cat1', 'cat2']}).apply()

        assert (repo / 'cat1' / 'file').read_text() == 'file2'
        assert (repo / 'cat2' / 'file').is_symlink()

    def test_restore_nomaster_nohome(self, tmp_path, caplog):
        home, repo = self.setup_home_repo(tmp_path)

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.restore({'file': ['cat1', 'cat2']}).apply()

        assert 'unable to find "file" in repo, skipping' in caplog.text
        assert not (home / 'file').is_file()

    def test_restore_nomaster_home(self, tmp_path, caplog):
        home, repo = self.setup_home_repo(tmp_path)
        open(home / 'file', 'w').close()

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.restore({'file': ['cat1', 'cat2']}).apply()

        assert 'unable to find "file" in repo, skipping' in caplog.text
        assert (home / 'file').is_file()

    def test_restore_master_nohome(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1')
        open(repo / 'cat1' / 'file', 'w').close()

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.restore({'file': ['cat1', 'cat2']}).apply()

        assert (home / 'file').is_file()
        assert (home / 'file').is_symlink()
        assert (home / 'file').samefile(repo / 'cat1' / 'file')
        assert not (repo / 'cat1' / 'file').is_symlink()

    def test_restore_master_linkedhome(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1')
        open(repo / 'cat1' / 'file', 'w').close()
        os.symlink(repo / 'cat1' / 'file', home / 'file')

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        fops = calc.restore({'file': ['cat1', 'cat2']})
        assert fops.ops == []

    def test_restore_master_home_replace(self, tmp_path, monkeypatch):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1')
        open(repo / 'cat1' / 'file', 'w').close()
        open(home / 'file', 'w').close()

        monkeypatch.setattr('builtins.input', lambda p: 'y')

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.restore({'file': ['cat1', 'cat2']}).apply()

        assert (home / 'file').is_file()
        assert (home / 'file').is_symlink()
        assert (home / 'file').samefile(repo / 'cat1' / 'file')
        assert not (repo / 'cat1' / 'file').is_symlink()

    def test_restore_master_home_noreplace(self, tmp_path, monkeypatch):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1')
        open(repo / 'cat1' / 'file', 'w').close()
        open(home / 'file', 'w').close()

        monkeypatch.setattr('builtins.input', lambda p: 'n')

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.restore({'file': ['cat1', 'cat2']}).apply()

        assert (home / 'file').is_file()
        assert not (home / 'file').is_symlink()
        assert (repo / 'cat1' / 'file').is_file()
        assert not (repo / 'cat1' / 'file').is_symlink()

    def test_restore_dangling_home(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat')
        (repo / 'cat' / 'foo').touch()

        (home / 'foo').symlink_to('/non/existent/path')
        assert not (home / 'foo').exists()

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.restore({'foo': ['cat']}).apply()

        assert (home / 'foo').is_symlink()
        assert (home / 'foo').exists()

    def test_clean_nohome(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1')
        open(repo / 'cat1' / 'file', 'w').close()

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.clean({'file': ['cat1', 'cat2']}).apply()

        assert not (home / 'file').is_file()
        assert (repo / 'cat1' / 'file').is_file()

    def test_clean_linkedhome(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1')
        open(repo / 'cat1' / 'file', 'w').close()
        os.symlink(repo / 'cat1' / 'file', home / 'file')

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.clean({'file': ['cat1', 'cat2']}).apply()

        assert not (home / 'file').is_file()
        assert (repo / 'cat1' / 'file').is_file()

    def test_clean_linkedotherhome(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1')
        open(repo / 'cat1' / 'file', 'w').close()
        os.symlink(Path('cat1') / 'file', home / 'file')

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.clean({'file': ['cat1', 'cat2']}).apply()

        assert (home / 'file').is_symlink()
        assert (repo / 'cat1' / 'file').is_file()

    def test_clean_filehome(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1')
        open(repo / 'cat1' / 'file', 'w').close()
        open(home / 'file', 'w').close()

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.clean({'file': ['cat1', 'cat2']}).apply()

        assert (home / 'file').is_file()
        assert not (home / 'file').is_symlink()
        assert (repo / 'cat1' / 'file').is_file()

    def test_clean_norepo_filehome(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        open(home / 'file', 'w').close()

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.clean({'file': ['cat1', 'cat2']}).apply()

        assert (home / 'file').is_file()
        assert not (home / 'file').is_symlink()
        assert not (repo / 'cat1' / 'file').exists()

    def test_clean_hard_nohome(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1')
        open(repo / 'cat1' / 'file', 'w').close()

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data', hard=True))
        calc.clean({'file': ['cat1', 'cat2']}).apply()

        assert not (home / 'file').is_file()
        assert (repo / 'cat1' / 'file').is_file()

    def test_clean_hard_linkedhome(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1')
        open(repo / 'cat1' / 'file', 'w').close()
        os.symlink(repo / 'cat1' / 'file', home / 'file')

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data', hard=True))
        calc.clean({'file': ['cat1', 'cat2']}).apply()

        # shouldn't remove symlinks since they are not hard-copied files from
        # the repo
        assert (home / 'file').is_file()
        assert (repo / 'cat1' / 'file').is_file()

    def test_clean_hard_filehome(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1')
        open(repo / 'cat1' / 'file', 'w').close()
        open(home / 'file', 'w').close()

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data', hard=True))
        calc.clean({'file': ['cat1', 'cat2']}).apply()

        assert not (home / 'file').is_file()
        assert (repo / 'cat1' / 'file').is_file()

    def test_clean_hard_difffilehome(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1')
        open(repo / 'cat1' / 'file', 'w').close()
        with open(home / 'file', 'w') as f:
            f.write('test data')

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data', hard=True))
        calc.clean({'file': ['cat1', 'cat2']}).apply()

        assert (home / 'file').is_file()
        assert (home / 'file').read_text() == 'test data'
        assert (repo / 'cat1' / 'file').is_file()

    def test_clean_repo(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1')
        open(repo / 'cat1' / 'file1', 'w').close()
        open(repo / 'cat1' / 'file2', 'w').close()
        os.makedirs(repo / 'cat2')
        open(repo / 'cat2' / 'file1', 'w').close()

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.clean_repo(['cat1/file1']).apply()

        assert (repo / 'cat1' / 'file1').is_file()
        assert not (repo / 'cat1' / 'file2').is_file()
        assert not (repo / 'cat2' / 'file2').is_file()

    def test_clean_repo_dirs(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1' / 'empty')
        assert (repo / 'cat1' / 'empty').is_dir()

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.clean_repo([]).apply()

        assert not (repo / 'cat1' / 'empty').is_dir()

    def test_clean_repo_categories(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1')
        assert (repo / 'cat1').is_dir()

        calc = CalcOps(repo, home, PlainPlugin(tmp_path / '.data'))
        calc.clean_repo([]).apply()

        assert not (repo / 'cat1').is_dir()
