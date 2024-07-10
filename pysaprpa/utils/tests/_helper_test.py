import unittest
import os
from pysaprpa.utils._helper import HelperUtils  # Replace 'your_module' with the actual module name

class TestHelperUtils(unittest.TestCase):
    def test_check_path_valid_existing_file(self):
        # Create a temporary directory and file for testing
        temp_dir = '/tmp/test_directory'
        temp_file = 'test_file.xlsx'
        os.makedirs(temp_dir, exist_ok=True)
        open(os.path.join(temp_dir, temp_file), 'w').close()

        # Initialize HelperUtils
        helper = HelperUtils()

        # Test existing file
        result = helper._check_path_valid('spreadsheet', temp_dir, temp_file)
        self.assertTrue(result)

        # Clean up
        os.remove(os.path.join(temp_dir, temp_file))
        os.rmdir(temp_dir)

        with self.assertRaises(ValueError):
            helper._check_path_valid('spreadsheet', temp_dir, temp_file)

    def test_clean_field_text(self):
        # Initialize HelperUtils
        helper = HelperUtils()

        # Test 1: Accented characters
        input_name = "ãäòábcd"
        expected_output = "aaoabcd"
        cleaned_name = helper._clean_field_text(input_name)
        self.assertEqual(cleaned_name, expected_output)

        # Test 2: Special characters
        input_name = "sold-by&and-for"
        expected_output = "sold_by_and_for"
        cleaned_name = helper._clean_field_text(input_name)
        self.assertEqual(cleaned_name, expected_output)

        # Test 3: Conjunctions
        input_name = "And"
        expected_output = 'and'
        cleaned_name = helper._clean_field_text(input_name)
        self.assertEqual(cleaned_name, expected_output)

        # Test 4: Normal text
        input_name = "Hello World"
        expected_output = "hello_world"
        cleaned_name = helper._clean_field_text(input_name)
        self.assertEqual(cleaned_name, expected_output)

        # Test 5: Empty string
        input_name = ""
        expected_output = ""
        cleaned_name = helper._clean_field_text(input_name)
        self.assertEqual(cleaned_name, expected_output)

    # Add more test methods for other functions as needed

if __name__ == '__main__':
    unittest.main()
