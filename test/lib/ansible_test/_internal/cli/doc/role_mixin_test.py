import os
import tempfile
import unittest
from ansible.lib.ansible.cli.doc import RoleMixin


class TestRoleMixin(unittest.TestCase):
    def setUp(self):
        """ Set up the test environment by creating a temporary directory and sample files. """
        self.mixin = RoleMixin()
        self.test_dir = tempfile.TemporaryDirectory()
        self.meta_dir = os.path.join(self.test_dir.name, 'meta')
        os.makedirs(self.meta_dir)

        # Create a sample YAML file
        self.spec_file = os.path.join(self.meta_dir, 'argument_specs.yml')
        with open(self.spec_file, 'w') as f:
            f.write("name: test_role")

    def tearDown(self):
        """ Clean up the temporary directory after each test. """
        self.test_dir.cleanup()

    def test_load_role_data_file_found(self):
        """ Test if data is loaded correctly when a valid role spec file is found. """
        result = self.mixin._load_role_data(self.test_dir.name, ['argument_specs.yml'], 'test_role', None)
        self.assertIn("name", result)
        self.assertEqual(result, "name: test_role")

    def test_load_role_data_file_not_found(self):
        """ Test if an empty dictionary is returned when the role spec file is not found. """
        result = self.mixin._load_role_data(self.test_dir.name, ['non_existent_file.yml'], 'test_role', None)
        self.assertEqual(result, {})

    def test_load_role_data_empty_file(self):
        """ Test if an empty dictionary is returned when the role spec file is empty. """
        empty_file = os.path.join(self.meta_dir, 'empty.yml')
        with open(empty_file, 'w') as f:
            f.write("")  # Write empty content

        result = self.mixin._load_role_data(self.test_dir.name, ['empty.yml'], 'test_role', None)
        self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main()

