"""
Quick usage examples for the Test Data Generator.
"""
from data_generator import TestDataGenerator, generate_test_data

# Example 1: Simple usage (one-liner)
generate_test_data("test_data_template.xlsx", "output.xlsx")


# Example 2: Using the class for more control
generator = TestDataGenerator("test_data_template.xlsx")
generator.load_template()

# Generate data as DataFrame
df = generator.generate()

# Inspect the data
print(df.head())
print(df.describe())

# Save to Excel
generator.save_to_excel("my_output.xlsx")


# Example 3: Generate data for multiple templates
templates = [
    ("employees_template.xlsx", "employees_data.xlsx"),
    ("products_template.xlsx", "products_data.xlsx"),
    ("transactions_template.xlsx", "transactions_data.xlsx"),
]

for template, output in templates:
    try:
        generate_test_data(template, output)
        print(f"Generated {output}")
    except Exception as e:
        print(f"Failed to generate {output}: {e}")
