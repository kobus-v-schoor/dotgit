from dotgit.__main__ import main
from dotgit.git import Git


class TestMain:
    def test_init(self, tmp_path, caplog):
        main(args=['init'], cwd=str(tmp_path))
        git = Git(str(tmp_path))

        assert (tmp_path / '.git').is_dir()
        assert (tmp_path / 'filelist').is_file()
        assert (tmp_path / '.gitignore').is_file()
        assert ((tmp_path / '.gitignore').read_text()
                =='.plugins/*/pre\n.plugins/*/post\n')
        assert git.last_commit() == 'Added .gitignore, added filelist'

        assert 'existing git repo' not in caplog.text
        assert 'existing filelist' not in caplog.text
        assert 'existing .gitignore' not in caplog.text

    def test_reinit(self, tmp_path, caplog):
        main(args=['init'], cwd=str(tmp_path))
        main(args=['init'], cwd=str(tmp_path))
        git = Git(str(tmp_path))

        assert (tmp_path / '.git').is_dir()
        assert (tmp_path / 'filelist').is_file()
        assert (tmp_path / '.gitignore').is_file()
        assert ((tmp_path / '.gitignore').read_text()
                =='.plugins/*/pre\n.plugins/*/post\n')
        assert git.last_commit() == 'Added .gitignore, added filelist'
        assert len(git.commits()) == 1

        assert 'existing git repo' in caplog.text
        assert 'existing filelist' in caplog.text
        assert 'existing .gitignore' in caplog.text
