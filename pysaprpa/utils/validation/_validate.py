from datetime import datetime
import calendar
from typing import Union

class ValidUtils():

    @staticmethod
    def _validate_date(date: str, date_format: str) -> bool:
        """
        Validate a date string in any format.

        Args:
            date (str): The date string to validate.
            date_format (str): The format of the date string (optional).

        Returns:
            bool: True if the date is valid, False otherwise.

        Raises:
            ValueError: If the date format is invalid or the month, day, or year is out of range.
        """
        try:
            dt = datetime.strptime(date, date_format)
        except ValueError:
            if date_format:
                raise ValueError(f"Invalid date format. Please use {date_format}")
            else:
                raise ValueError("Invalid date format")

        return True

    @staticmethod
    def _first_last_day(month: int, year: int, date_format: str) -> tuple:
        """
        Get the first and last day of a month.

        Args:
            month (int): The month.
            year (int): The year.

        Returns:
            tuple: A tuple containing the first and last day of the month in MM/DD/YYYY format.

        Raises:
            ValueError: If the month or year is out of range.
        """
        if not (1 <= month <= 12):
            raise ValueError("Invalid month. Must be between 1 and 12")
        if not (1900 <= year <= datetime.now().year):
            raise ValueError("Invalid year. Must be between 1900 and the current year")

        date = datetime(year, month, 1)
        first_date = date.strftime(date_format)
        last_day = calendar.monthrange(year, month)[1]
        last_date = datetime(year, month, last_day)
        last_date = last_date.strftime(date_format)

        return first_date, last_date

    @staticmethod
    def _check_date_valid(date: Union[str, tuple], i: int, date_format: str) -> str:
        """
        Validate a date or a month/year tuple and return a valid date string.

        Args:
            date (Union[str, tuple]): The date or month/year tuple to validate.
            i (int): An index indicating whether to return the first or last day of the month.

        Returns:
            str: A valid date string in MM/DD/YYYY format.

        Raises:
            ValueError: If the date or month/year tuple is invalid.
        """
        if isinstance(date, str):
            if date != '':
                ValidUtils._validate_date(date, date_format)
        else:
            if i == 0:
                date, _ = ValidUtils._first_last_day(month=date[0], year=date[1], date_format=date_format)
            else:
                _, date = ValidUtils._first_last_day(month=date[0], year=date[1], date_format=date_format)
        
        return date