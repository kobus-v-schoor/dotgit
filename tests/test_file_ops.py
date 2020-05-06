import os

from dotgit.file_ops import FileOps, Op

class TestFileOps:
    def test_init(self, tmp_path):
        fop = FileOps(tmp_path)
        assert fop.wd == tmp_path

    def test_check_dest_dir(self, tmp_path):
        fop = FileOps(tmp_path)

        # check relative path directly in wd
        fop.check_dest_dir('file')
        assert fop.ops == []
        fop.clear()

        # check relative path with non-existent dir
        fop.check_dest_dir(os.path.join('dir', 'file'))
        assert fop.ops == [(Op.MKDIR, 'dir')]
        fop.clear()

        dirname = os.path.join(tmp_path, 'dir')

        # check relative path with existent dir
        os.makedirs(dirname)
        fop.check_dest_dir(os.path.join('dir', 'file'))
        assert fop.ops == []
        fop.clear()
        os.rmdir(dirname)

        # check abs path with non-existent dir
        fop.check_dest_dir(os.path.join(dirname, 'file'))
        assert fop.ops == [(Op.MKDIR, dirname)]
        fop.clear()

        # check absolute path with existent dir
        os.makedirs(dirname)
        fop.check_dest_dir(os.path.join(dirname, 'file'))
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

    def test_apply(self, tmp_path):
        ## test the creating of the following structure (x marks existing files)
        # dir1 (x)
        #  -> file1 (x)
        # delete_file (x) (will be deleted)
        # delete_folder (x) (will be deleted)
        #  -> file (x) (will be deleted)
        # rename (x) (will be renamed to "renamed")
        #
        # link1 -> dir1/file1
        # link_dir/link2 -> ../dir1/file1
        # new_dir
        # copy_dir
        # -> copy_dir/file (from dir1/file1)

        os.makedirs(tmp_path / 'dir1')
        open(tmp_path / 'dir1' / 'file1', 'w').close()
        open(tmp_path / 'delete_file', 'w').close()
        os.makedirs(tmp_path / 'delete_folder')
        open(tmp_path / 'delete_folder' / 'file', 'w').close()
        open(tmp_path / 'rename', 'w').close()

        fop = FileOps(tmp_path)

        fop.remove('delete_file')
        fop.remove('delete_folder')

        fop.move('rename', 'renamed')

        fop.link(tmp_path / 'dir1' / 'file1', 'link1')
        fop.link(tmp_path / 'dir1' / 'file1', os.path.join('link_dir', 'link1'))

        fop.mkdir('new_dir')

        fop.copy(os.path.join('dir1','file1'), os.path.join('copy_dir', 'file'))

        fop.apply()

        assert not os.path.isfile(tmp_path / 'delete_file')
        assert not os.path.isfile(tmp_path / 'delete_folder' / 'file')
        assert not os.path.isdir(tmp_path / 'delete_folder')

        assert not os.path.isfile(tmp_path / 'rename')
        assert os.path.isfile(tmp_path / 'renamed')

        assert os.path.islink(tmp_path / 'link1')
        assert os.readlink(tmp_path / 'link1') == os.path.join('dir1', 'file1')
        assert os.path.isdir(tmp_path / 'link_dir')
        assert os.path.islink(tmp_path / 'link_dir' / 'link1')
        assert (os.readlink(tmp_path / 'link_dir' / 'link1') ==
                os.path.join('..', 'dir1', 'file1'))

        assert os.path.isdir(tmp_path / 'new_dir')

        assert os.path.isdir(tmp_path / 'copy_dir')
        assert os.path.isfile(tmp_path / 'copy_dir' / 'file')
        assert not os.path.islink(tmp_path / 'copy_dir' / 'file')
