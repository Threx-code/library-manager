import unittest
import tempfile
import os
from library_manager import LibraryManager

tmp_data = b"""
A depends on B C
B depends on C E
C depends on G
D depends on A F
E depends on F
F depends on H
"""

class TestLibraryManager(unittest.TestCase):
    def setUp(self):
        self.tmp_file = tempfile.NamedTemporaryFile(delete=False)
        self.tmp_file.write(tmp_data)
        self.tmp_file.close()
        self.library_manager = LibraryManager(self.tmp_file.name)


    def tearDown(self):
        os.remove(self.tmp_file.name)


    def test_parse_dependencies(self):
        expected_output = "A depends on B, C, E, F, G, H\nB depends on C, E, F, G, H\nC depends on G\nD depends on A, B, C, E, F, G, H\nE depends on F, H\nF depends on H\n"
        output = self.library_manager.parse_dependencies()
        self.assertEqual(output, expected_output)


    def test_file_not_found(self):
        self.library_manager.file_path = "file_not_found.txt"
        output = self.library_manager.parse_dependencies()
        self.assertEqual(output, self.library_manager.FILE_NOT_FOUND_ERROR)


if __name__ == "__main__":
    unittest.main()
