# Test Data Generator Tool

A flexible Python tool for generating test/dummy data based on Excel templates with customizable rules.

## Features

- **14 data types** supported (integers, decimals, names, emails, dates, addresses, etc.)
- **Pattern-based generation** for custom formats (e.g., ACC-12345, PRD-###-ABCD)
- **Unique constraints** for IDs and codes
- **Date/datetime ranges** with custom formatting
- **Choice lists** for predefined options
- **International support** for postal codes and addresses
- **Easy to extend** with modular architecture

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

Generate test data using the default template:

```bash
python main.py
```

This will read `test_data_template.xlsx` and generate `test_data_output.xlsx`.

### Custom Files

Specify custom template and output files:

```bash
python main.py -t my_template.xlsx -o my_output.xlsx
```

### Command Line Options

```bash
python main.py --help
```

Options:
- `-t, --template`: Path to template Excel file (default: `test_data_template.xlsx`)
- `-o, --output`: Path for output Excel file (default: `test_data_output.xlsx`)

## Template Format

Your Excel template must have two columns:

1. **Column Name**: Name of the column in the output file
2. **Rule**: Rule string defining how to generate data

### Special First Row

The first row specifies the number of data rows to generate:

| Column Name | Rule |
|-------------|------|
| Number of data rows | 100 |

### Example Template

| Column Name | Rule |
|-------------|------|
| Number of data rows | 100 |
| employee_id | type:integer; range:1000-9999; unique:true |
| first_name | type:first_name |
| email | type:email; domain:company.com |
| salary | type:decimal; range:45000-150000; precision:2 |
| department | type:choice; values:HR,Finance,IT,Sales |

## Supported Data Types

### 1. Integer
```
type:integer; range:1000-9999; unique:true
```
- `range`: min-max values (required)
- `unique`: true/false (optional)

### 2. Decimal
```
type:decimal; range:45000-150000; precision:2
```
- `range`: min-max values (required)
- `precision`: decimal places (optional, default: 2)

### 3. String (Pattern-based)
```
type:string; pattern:ACC-#####; unique:true
```
Pattern symbols:
- `#` = digit (0-9)
- `@` = uppercase letter (A-Z)
- `?` = lowercase letter (a-z)
- `*` = alphanumeric

### 4. First Name
```
type:first_name
```

### 5. Last Name
```
type:last_name
```

### 6. Email
```
type:email; domain:company.com
```
- `domain`: email domain (optional, default: example.com)

### 7. Phone
```
type:phone; format:###-###-####
```
- `format`: phone format using # for digits

### 8. Date
```
type:date; start:2020-01-01; end:2024-12-31; format:%Y-%m-%d
```
- `start`: start date (required)
- `end`: end date (required)
- `format`: date format (optional)

### 9. Datetime
```
type:datetime; start:2024-01-01; end:2024-12-31; format:%Y-%m-%d %H:%M:%S
```

### 10. Boolean
```
type:boolean
```

### 11. Choice
```
type:choice; values:HR,Finance,IT,Sales,Operations
```
- `values`: comma-separated list (required)

### 12. Address
```
type:address
```

### 13. Postal Code
```
type:postal_code; country:CA
```
- `country`: country code (US, CA, UK, etc.)

### 14. Text
```
type:text; words:5-15
```
- `words`: range of words (optional, default: 5-10)

## Project Structure

```
.
├── main.py                      # Entry point
├── data_generator.py            # Main orchestrator
├── generators.py                # Data type generators
├── rule_parser.py              # Rule parsing logic
├── requirements.txt            # Dependencies
├── test_data_template.xlsx     # Example template
└── RULE_SPECIFICATION.txt      # Detailed rule documentation
```

## Usage Examples

### Example 1: Employee Data
```
Column Name: employee_id
Rule: type:integer; range:10000-99999; unique:true

Column Name: full_name
Rule: type:first_name

Column Name: hire_date
Rule: type:date; start:2020-01-01; end:2024-12-31; format:%Y-%m-%d
```

### Example 2: Transaction Data
```
Column Name: transaction_id
Rule: type:string; pattern:TXN-#######; unique:true

Column Name: amount
Rule: type:decimal; range:10.00-5000.00; precision:2

Column Name: status
Rule: type:choice; values:Completed,Pending,Failed,Cancelled
```

### Example 3: Product Codes
```
Column Name: product_code
Rule: type:string; pattern:PRD-###-@@@@; unique:true

Column Name: description
Rule: type:text; words:10-20
```

## Extending the Tool

To add a new data type:

1. Add generator function in `generators.py`:
```python
def generate_my_type(params, n):
    # Your generation logic
    return [generated_value for _ in range(n)]
```

2. Register it in `data_generator.py`:
```python
TYPE_GENERATORS = {
    # ... existing types
    "my_type": generate_my_type,
}
```

3. Use it in your template:
```
type:my_type; param1:value1; param2:value2
```

## Error Handling

The tool provides helpful error messages:
- Missing required parameters
- Invalid data types
- Unique constraint violations
- File not found errors

## License

MIT License - feel free to use and modify for your needs.

## Contributing

Contributions welcome! Feel free to:
- Add new data types
- Improve error handling
- Add validation features
- Enhance documentation
