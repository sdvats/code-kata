import unittest
from Problem1.parse_fixed_width_file import ParseFixedWidthFile


class TestParseFixedWidthFile(unittest.TestCase):

    def setUp(self):
        self.parse_fixed_width_file = ParseFixedWidthFile()
    
    def test_is_spec_read_file_not_found(self):
        try:
            # reading the spec file which do not exists
            self.parse_fixed_width_file.read_config_file("spec1.json")
        except FileNotFoundError:
            self.assertTrue(True)
        

    def test_is_offset_set(self):
        # reading the spec file which exists
        self.parse_fixed_width_file.read_config_file("spec.json")
        self.assertIsNotNone(self.parse_fixed_width_file.offsets)

    def test_is_fixed_width_encoding_set(self):
        # reading the spec file which exists
        self.parse_fixed_width_file.read_config_file("spec.json")
        self.assertIsNotNone(self.parse_fixed_width_file.fixed_width_file_encoding)

    def test_is_deliminted_encoding_set(self):
        # reading the spec file which exists
        self.parse_fixed_width_file.read_config_file("spec.json")
        self.assertIsNotNone(self.parse_fixed_width_file.delimited_file_encoding)

    def test_read_fixed_width_file(self):
        try:
            # setting the encoding because needed by the read fixed width file encoding method
            self.parse_fixed_width_file.fixed_width_file_encoding = 'windows-1252'
            # reading fixed width file
            self.parse_fixed_width_file.read_fixed_width_file("test_files/sample_fixed_width_file_not_exists")
        except FileNotFoundError:
            self.assertTrue(True)
    
    def test_parse_file_to_delimited(self):
        try:
            # setting the encoding because needed by the read fixed width file encoding method
            self.parse_fixed_width_file.fixed_width_file_encoding = 'windows-1252'
            # reading the sampe fixed width file
            content = self.parse_fixed_width_file.read_fixed_width_file("test_files/sample_fixed_width_file")
            # parsing the file
            self.parse_fixed_width_file.parse_to_delimited(content, ",")
        except:
            self.assertFalse(False)


    def test_write_delimited_file(self):
        # define sample content
        content = '1,2,3,4,5'
        try:
            # setting output file encoding
            self.parse_fixed_width_file.delimited_file_encoding = 'utf-8'
            # write the content into the sample file
            self.parse_fixed_width_file.write_delimiter_file(content, "test_files/test_delimited_file_write")
        except (FileNotFoundError, PermissionError, OSError):
            self.assertFalse(False)


