"""
Main data generator module that orchestrates the test data generation process.
"""
import pandas as pd
from rule_parser import parse_rule, validate_rule
from generators import (
    generate_integer, generate_decimal, generate_string,
    generate_first_name, generate_last_name, generate_email,
    generate_phone, generate_date, generate_datetime,
    generate_boolean, generate_choice, generate_address,
    generate_postal_code, generate_text
)


class TestDataGenerator:
    """Main class for generating test data from Excel templates."""

    # Map data types to their generator functions
    TYPE_GENERATORS = {
        "integer": generate_integer,
        "decimal": generate_decimal,
        "string": generate_string,
        "first_name": generate_first_name,
        "last_name": generate_last_name,
        "email": generate_email,
        "phone": generate_phone,
        "date": generate_date,
        "datetime": generate_datetime,
        "boolean": generate_boolean,
        "choice": generate_choice,
        "address": generate_address,
        "postal_code": generate_postal_code,
        "text": generate_text,
    }

    def __init__(self, template_path):
        """
        Initialize the generator with a template file.

        Args:
            template_path (str): Path to the Excel template file
        """
        self.template_path = template_path
        self.df = None
        self.n_rows = 0
        self.columns = []
        self.rules = []

    def load_template(self):
        """Load and parse the Excel template."""
        try:
            self.df = pd.read_excel(self.template_path)

            # First row contains the number of rows to generate
            self.n_rows = int(self.df.iloc[0, 1])

            # Remaining rows contain column definitions
            self.columns = self.df.loc[1:, "Column Name"].tolist()
            self.rules = self.df.loc[1:, "Rule"].tolist()

            print(f"Template loaded: {len(self.columns)} columns, {self.n_rows} rows to generate")

        except Exception as e:
            raise ValueError(f"Error loading template: {str(e)}")

    def generate_column_data(self, column_name, rule):
        """
        Generate data for a single column based on its rule.

        Args:
            column_name (str): Name of the column
            rule (str): Rule string defining data generation

        Returns:
            list: Generated data for the column
        """
        params = parse_rule(rule)

        # Validate the rule
        is_valid, error_msg = validate_rule(params)
        if not is_valid:
            print(f"Warning: Invalid rule for column '{column_name}': {error_msg}")
            return [""] * self.n_rows

        data_type = params.get("type")

        if data_type not in self.TYPE_GENERATORS:
            print(f"Warning: Unknown type '{data_type}' for column '{column_name}'")
            return [""] * self.n_rows

        try:
            generator = self.TYPE_GENERATORS[data_type]
            return generator(params, self.n_rows)
        except Exception as e:
            print(f"Error generating data for column '{column_name}': {str(e)}")
            return [""] * self.n_rows

    def generate(self):
        """
        Generate all data based on the template.

        Returns:
            pd.DataFrame: Generated test data
        """
        if self.df is None:
            self.load_template()

        data_dict = {}

        print(f"\nGenerating data...")
        for i, (col, rule) in enumerate(zip(self.columns, self.rules), 1):
            print(f"  [{i}/{len(self.columns)}] Generating '{col}'...")
            data_dict[col] = self.generate_column_data(col, rule)

        return pd.DataFrame(data_dict)

    def save_to_excel(self, output_path):
        """
        Generate data and save to Excel file.

        Args:
            output_path (str): Path for the output Excel file
        """
        df_output = self.generate()
        df_output.to_excel(output_path, index=False)
        print(f"\nSuccessfully generated {len(df_output)} rows")
        print(f"Output saved to: {output_path}")

        # Print summary
        print(f"\nSummary:")
        print(f"   - Columns: {len(df_output.columns)}")
        print(f"   - Rows: {len(df_output)}")
        print(f"   - File size: {self._get_file_size(output_path)}")

    @staticmethod
    def _get_file_size(filepath):
        """Get human-readable file size."""
        import os
        size_bytes = os.path.getsize(filepath)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"


def generate_test_data(template_path, output_path):
    """
    Convenience function to generate test data in one call.

    Args:
        template_path (str): Path to Excel template file
        output_path (str): Path for output Excel file
    """
    generator = TestDataGenerator(template_path)
    generator.save_to_excel(output_path)
