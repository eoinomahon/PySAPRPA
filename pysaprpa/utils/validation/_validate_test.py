import unittest
from _validate import ValidUtils

class TestValidUtils(unittest.TestCase):
    def test_validate_date_valid(self):
        # Valid date format (MM/DD/YYYY)
        self.assertTrue(ValidUtils._validate_date("05/15/2023", "%m/%d/%Y"))

    def test_validate_date_invalid_format(self):
        # Invalid date format
        with self.assertRaises(ValueError):
            ValidUtils._validate_date("2023-05-15", "%m/%d/%Y")

    def test_first_last_day_valid(self):
        # Valid month and year
        first_day, last_day = ValidUtils._first_last_day(month=5, year=2023, date_format="%m/%d/%Y")
        self.assertEqual(first_day, "05/01/2023")
        self.assertEqual(last_day, "05/31/2023")

    def test_first_last_day_invalid_month(self):
        # Invalid month (13)
        with self.assertRaises(ValueError):
            ValidUtils._first_last_day(month=13, year=2023, date_format="%m/%d/%Y")

    def test_first_last_day_invalid_year(self):
        # Invalid year (1899)
        with self.assertRaises(ValueError):
            ValidUtils._first_last_day(month=5, year=1899, date_format="%m/%d/%Y")

    def test_check_date_valid_string(self):
        # Valid date string
        result = ValidUtils._check_date_valid("05/15/2023", i=0, date_format="%m/%d/%Y")
        self.assertEqual(result, "05/15/2023")

    def test_check_date_valid_tuple(self):
        # Valid month/year tuple
        result = ValidUtils._check_date_valid((5, 2023), i=1, date_format="%m/%d/%Y")
        self.assertEqual(result, "05/31/2023")

    def test_check_date_invalid_tuple(self):
        # Invalid month/year tuple (month=13)
        with self.assertRaises(ValueError):
            ValidUtils._check_date_valid((13, 2023), i=1, date_format="%m/%d/%Y")

if __name__ == '__main__':
    unittest.main()
