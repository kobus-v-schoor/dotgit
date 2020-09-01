import os
from dotgit.__main__ import main

# meant to test basic usage patterns
class TestIntegration:
    def setup_repo(self, tmp_path, flist):
        home = tmp_path / 'home'
        repo = tmp_path / 'repo'
        os.makedirs(home)
        os.makedirs(repo)
        main(args=['init'], cwd=str(repo))
        with open(repo / 'filelist', 'w') as f:
            f.write(flist)

        return home, repo

    def test_add_to_flist(self, tmp_path):
        home, repo = self.setup_repo(tmp_path, "")
        filelist = repo / "filelist"

        filelist.write_text("foo")
        main(args=['update'], cwd=str(repo), home=str(home))
        assert not (repo / "dotfiles").is_dir()

        (home / "foo").touch()
        main(args=['update'], cwd=str(repo), home=str(home))
        assert (repo / "dotfiles").is_dir()
        assert (home / "foo").is_symlink()
        assert (home / "foo").exists()

        filelist.write_text("foo\nbar")
        main(args=['update'], cwd=str(repo), home=str(home))
        assert (repo / "dotfiles").is_dir()

        (home / "bar").touch()
        main(args=['update'], cwd=str(repo), home=str(home))
        assert (home / "foo").is_symlink()
        assert (home / "foo").exists()
        assert (home / "bar").is_symlink()
        assert (home / "bar").exists()
