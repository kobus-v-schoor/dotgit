import os

from dotgit.file_ops import FileOps, Op

class TestFileOps:
    def test_init(self, tmp_path):
        fop = FileOps(tmp_path)
        assert fop.wd == tmp_path

    def test_check_dest_dir(self, tmp_path):
        fop = FileOps(tmp_path)

        # check relative path directly in wd
        assert not fop.check_dest_dir('file')
        assert fop.ops == []
        fop.clear()

        # check relative path with non-existent dir
        assert fop.check_dest_dir(os.path.join('dir', 'file'))
        assert fop.ops == [(Op.MKDIR, 'dir')]
        fop.clear()

        dirname = os.path.join(tmp_path, 'dir')

        # check relative path with existent dir
        os.makedirs(dirname)
        assert not fop.check_dest_dir(os.path.join('dir', 'file'))
        assert fop.ops == []
        fop.clear()
        os.rmdir(dirname)

        # check abs path with non-existent dir
        assert fop.check_dest_dir(os.path.join(dirname, 'file'))
        assert fop.ops == [(Op.MKDIR, dirname)]
        fop.clear()

        # check absolute path with existent dir
        os.makedirs(dirname)
        assert not fop.check_dest_dir(os.path.join(dirname, 'file'))
        assert fop.ops == []

    def test_mkdir(self, tmp_path):
        fop = FileOps(tmp_path)
        fop.mkdir('dir')
        assert fop.ops == [(Op.MKDIR, 'dir')]

    def test_copy(self, tmp_path):
        fop = FileOps(tmp_path)

        # existing dest dir
        fop.copy('from', 'to')
        assert fop.ops == [(Op.COPY, ('from', 'to'))]
        fop.clear()

        # non-existing dest dir
        dest = os.path.join('dir', 'to')
        fop.copy('from', dest)
        assert fop.ops == [(Op.MKDIR, 'dir'), (Op.COPY, ('from', dest))]

    def test_move(self, tmp_path):
        fop = FileOps(tmp_path)

        # existing dest dir
        fop.move('from', 'to')
        assert fop.ops == [(Op.MOVE, ('from', 'to'))]
        fop.clear()

        # non-existing dest dir
        dest = os.path.join('dir', 'to')
        fop.move('from', dest)
        assert fop.ops == [(Op.MKDIR, 'dir'), (Op.MOVE, ('from', dest))]

    def test_link(self, tmp_path):
        fop = FileOps(tmp_path)

        # existing dest dir
        fop.link('from', 'to')
        assert fop.ops == [(Op.LINK, ('from', 'to'))]
        fop.clear()

        # non-existing dest dir
        dest = os.path.join('dir', 'to')
        fop.link('from', dest)
        assert fop.ops == [(Op.MKDIR, 'dir'), (Op.LINK, ('from', dest))]

    def test_remove(self, tmp_path):
        fop = FileOps(tmp_path)
        fop.remove('file')
        assert fop.ops == [(Op.REMOVE, 'file')]

    def test_str(self, tmp_path):
        fop = FileOps(tmp_path)
        fop.copy('foo', 'bar')
        fop.remove('file')
        assert str(fop) == 'COPY "foo" -> "bar"\nREMOVE "file"'
