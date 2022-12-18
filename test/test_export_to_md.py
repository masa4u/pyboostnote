import unittest
import shutil
import os
from tempfile import mkdtemp

from boostnote.base import Boostnote
from boostnote.exporter.markdown import export_boostnote, AttachPathType
import tarfile


def extract_file(path):
    filename = os.path.join(os.path.dirname(__file__), 'sample', 'boostnote.tar.gz')

    with tarfile.open(filename, 'r:gz') as fp:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(fp, path)


class TestExportToMD(unittest.TestCase):

    def setUp(self):
        self.source_path = mkdtemp()
        self.target_link_relative_path = mkdtemp()
        self.target_copy_md_path = mkdtemp()
        self.target_copy_sub_path = mkdtemp()
        extract_file(self.source_path)

    def tearDown(self) -> None:
        shutil.rmtree(self.source_path)
        shutil.rmtree(self.target_link_relative_path)
        shutil.rmtree(self.target_copy_md_path)
        shutil.rmtree(self.target_copy_sub_path)

    def test_storage_migration_link_relative(self):
        boostnote = Boostnote([self.source_path])
        storage = boostnote.storages['Default0']

        target_path = self.target_link_relative_path
        export_boostnote(storage, self.target_link_relative_path, AttachPathType.LinkRelativePath)

        folders = os.listdir(target_path)
        folders.sort()
        self.assertEqual(['Default', 'ffff'], folders)

        default_folder = os.listdir(os.path.join(target_path, 'Default'))
        self.assertTrue('Welcome to Boostnote!.md' in default_folder)

        attach_folder = os.listdir(os.path.join(target_path, 'Default', 'Welcome to Boostnote!'))
        self.assertEqual(['983eee58.png'], attach_folder)

    def test_storage_migration_copy_md_path(self):
        boostnote = Boostnote([self.source_path])
        storage = boostnote.storages['Default0']

        target_path = self.target_copy_md_path
        export_boostnote(storage, target_path, AttachPathType.CopyToMarkdownPath)

        default_folder = os.listdir(os.path.join(target_path, 'Default'))
        self.assertTrue(len(default_folder) == 5)

    def test_storage_migration_copy_sub_md_path(self):
        boostnote = Boostnote([self.source_path])
        storage = boostnote.storages['Default0']

        target_path = self.target_copy_sub_path
        export_boostnote(storage, target_path, AttachPathType.CopyToMarkdownSubPath)

        default_folder = os.listdir(os.path.join(target_path, 'Default'))
        self.assertTrue(len(default_folder) == 4)


if __name__ == '__main__':
    unittest.main()
