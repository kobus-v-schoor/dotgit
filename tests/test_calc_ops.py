import os

from dotgit.calc_ops import CalcOps
from dotgit.file_ops import FileOps

class TestCalcOps:
    def setup_home_repo(self, tmp_path):
        os.makedirs(tmp_path / 'home')
        os.makedirs(tmp_path / 'repo')
        return tmp_path/'home', tmp_path/'repo'

    def test_update_no_cands(self, tmp_path, caplog):
        home, repo = self.setup_home_repo(tmp_path)
        calc = CalcOps(repo, home)
        calc.update({'file': ['cat1', 'cat2']})
        assert 'unable to find any candidates' in caplog.text

    def test_update_master_noslave(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat1')
        open(repo / 'cat1' / 'file', 'w').close()

        calc = CalcOps(repo, home)
        calc.update({'file': ['cat1', 'cat2']}).apply()

        assert not (repo / 'cat1' / 'file').is_symlink()
        assert (repo / 'cat2').is_dir()
        assert (repo / 'cat2' / 'file').is_symlink()
        assert (repo / 'cat2' / 'file').samefile(repo / 'cat1' / 'file')

    def test_update_nomaster_slave(self, tmp_path):
        home, repo = self.setup_home_repo(tmp_path)
        os.makedirs(repo / 'cat2')
        open(repo / 'cat2' / 'file', 'w').close()

        calc = CalcOps(repo, home)
        calc.update({'file': ['cat1', 'cat2']}).apply()

        assert not (repo / 'cat1' / 'file').is_symlink()
        assert (repo / 'cat2').is_dir()
        assert (repo / 'cat2' / 'file').is_symlink()
        assert (repo / 'cat2' / 'file').samefile(repo / 'cat1' / 'file')
