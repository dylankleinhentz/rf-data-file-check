"""
CSV Data File Validator Library
Validates CSV data against business requirements
"""

import csv
import re
from robot.api.deco import keyword
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple


def __init__(self):
    self.data = []
    self.errors = []
    self.warnings = []
    self.current_file = None


class file_validation:
    def load_csv_file(self, file_path: str) -> bool:
        """
        Load a CSV file for validation

        Args:
            file_path: Path to the CSV file

        Returns:
            True if file loaded successfully, False otherwise
        """
        try:
            self.current_file = file_path
            self.data = []
            self.errors = []
            self.warnings = []

            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.data = list(reader)

            return True
        except FileNotFoundError:
            self.errors.append(f"File not found: {file_path}")
            return False
        except Exception as e:
            self.errors.append(f"Error loading file: {str(e)}")
            return False

    def validate_column_exists(self, column_name: str) -> bool:
        """
        Validate that a column exists in the CSV

        Args:
            column_name: Name of the column to check

        Returns:
            True if column exists, False otherwise
        """
        if not self.data:
            self.errors.append("No data loaded")
            return False

        if column_name not in self.data[0]:
            self.errors.append(f"Column '{column_name}' not found")
            return False

        return True

    def validate_required_columns(self, columns: List[str]) -> bool:
        """
        Validate that all required columns exist and have no empty values

        Args:
            columns: List of required column names

        Returns:
            True if all validations pass, False otherwise
        """
        all_valid = True

        for column in columns:
            if not self.validate_column_exists(column):
                all_valid = False
                continue

            empty_rows = []
            for idx, row in enumerate(self.data, 1):
                if not row[column] or row[column].strip() == '':
                    empty_rows.append(idx)

            if empty_rows:
                self.errors.append(
                    f"Column '{column}' has empty values in rows: {empty_rows}"
                )
                all_valid = False

        return all_valid

    def validate_column_data_type(self, column_name: str, data_type: str) -> bool:
        """
        Validate data type for a column

        Args:
            column_name: Name of the column
            data_type: Expected data type ('numeric', 'string', 'date')

        Returns:
            True if all values match the data type, False otherwise
        """
        if not self.validate_column_exists(column_name):
            return False

        invalid_rows = []

        for idx, row in enumerate(self.data, 1):
            value = row[column_name]
            if not value or value.strip() == '':
                continue

            if data_type == 'numeric':
                if not self._is_numeric(value):
                    invalid_rows.append((idx, value))
            elif data_type == 'date':
                if not self._is_date(value):
                    invalid_rows.append((idx, value))
            # 'string' type accepts any value

        if invalid_rows:
            self.errors.append(
                f"Column '{column_name}' has invalid {data_type} values: {invalid_rows}"
            )
            return False

        return True

    def validate_unique_values(self, column_name: str) -> bool:
        """
        Validate that all values in a column are unique

        Args:
            column_name: Name of the column

        Returns:
            True if all values are unique, False otherwise
        """
        if not self.validate_column_exists(column_name):
            return False

        values = []
        duplicates = {}

        for idx, row in enumerate(self.data, 1):
            value = row[column_name]
            if value and value.strip():
                if value in values:
                    if value not in duplicates:
                        duplicates[value] = []
                    duplicates[value].append(idx)
                values.append(value)

        if duplicates:
            dup_str = ', '.join(
                [f"'{k}' (rows {v})" for k, v in duplicates.items()])
            self.errors.append(
                f"Column '{column_name}' has duplicate values: {dup_str}"
            )
            return False

        return True

    def validate_value_range(self, column_name: str, min_value: float = None,
                             max_value: float = None) -> bool:
        """
        Validate numeric values fall within a range

        Args:
            column_name: Name of the column
            min_value: Minimum allowed value (inclusive)
            max_value: Maximum allowed value (inclusive)

        Returns:
            True if all values are within range, False otherwise
        """
        if not self.validate_column_exists(column_name):
            return False

        out_of_range = []

        for idx, row in enumerate(self.data, 1):
            value = row[column_name]
            if not value or value.strip() == '':
                continue

            try:
                num_value = float(value)
                if min_value is not None and num_value < min_value:
                    out_of_range.append((idx, value, f"less than {min_value}"))
                elif max_value is not None and num_value > max_value:
                    out_of_range.append(
                        (idx, value, f"greater than {max_value}"))
            except ValueError:
                pass

        if out_of_range:
            err_str = ', '.join(
                [f"row {r[0]}='{r[1]}' ({r[2]})" for r in out_of_range])
            self.errors.append(
                f"Column '{column_name}' has out-of-range values: {err_str}"
            )
            return False

        return True

    def validate_pattern(self, column_name: str, pattern: str) -> bool:
        """
        Validate values match a regex pattern

        Args:
            column_name: Name of the column
            pattern: Regex pattern to match

        Returns:
            True if all values match the pattern, False otherwise
        """
        if not self.validate_column_exists(column_name):
            return False

        invalid_rows = []

        try:
            regex = re.compile(pattern)
        except re.error as e:
            self.errors.append(f"Invalid regex pattern: {str(e)}")
            return False

        for idx, row in enumerate(self.data, 1):
            value = row[column_name]
            if not value or value.strip() == '':
                continue

            if not regex.match(value):
                invalid_rows.append((idx, value))

        if invalid_rows:
            err_str = ', '.join([f"row {r[0]}='{r[1]}'" for r in invalid_rows])
            self.errors.append(
                f"Column '{column_name}' values don't match pattern '{pattern}': {err_str}"
            )
            return False

        return True

    def get_row_count(self) -> int:
        """Get the number of data rows loaded"""
        return len(self.data)

    def get_column_names(self) -> List[str]:
        """Get list of column names"""
        if self.data:
            return list(self.data[0].keys())
        return []

    def get_errors(self) -> List[str]:
        """Get list of validation errors"""
        return self.errors

    def get_warnings(self) -> List[str]:
        """Get list of validation warnings"""
        return self.warnings

    def get_all_messages(self) -> Dict[str, List[str]]:
        """Get all validation messages"""
        return {
            'errors': self.errors,
            'warnings': self.warnings
        }

    def clear_messages(self) -> None:
        """Clear all error and warning messages"""
        self.errors = []
        self.warnings = []

    @staticmethod
    def _is_numeric(value: str) -> bool:
        """Check if value is numeric"""
        try:
            float(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def _is_date(value: str) -> bool:
        """Check if value is a date (basic check)"""
        date_patterns = [
            r'^\d{4}-\d{2}-\d{2}$',
            r'^\d{2}/\d{2}/\d{4}$',
            r'^\d{2}-\d{2}-\d{4}$',
        ]
        return any(re.match(pattern, value) for pattern in date_patterns)
