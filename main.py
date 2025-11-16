"""
Main entry point for the Test Data Generator Tool.
Run this script to generate test data from your template.
"""
import sys
import argparse
from data_generator import generate_test_data


def main():
    """Main function with command-line argument parsing."""
    parser = argparse.ArgumentParser(
        description='Generate test data from Excel template',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Uses default files
  python main.py -t my_template.xlsx                # Custom template
  python main.py -t template.xlsx -o output.xlsx    # Custom input and output
  python main.py --template data.xlsx --output test_data.xlsx
        """
    )

    parser.add_argument(
        '-t', '--template',
        default='test_data_template.xlsx',
        help='Path to the Excel template file (default: test_data_template.xlsx)'
    )

    parser.add_argument(
        '-o', '--output',
        default='test_data_output.xlsx',
        help='Path for the output Excel file (default: test_data_output.xlsx)'
    )

    args = parser.parse_args()

    print("="*70)
    print("TEST DATA GENERATOR TOOL")
    print("="*70)
    print(f"Template: {args.template}")
    print(f"Output:   {args.output}")
    print("="*70)

    try:
        generate_test_data(args.template, args.output)
        print("="*70)
        print("✨ Generation completed successfully!")
        print("="*70)
        return 0
    except FileNotFoundError:
        print(f"\nError: Template file '{args.template}' not found")
        return 1
    except Exception as e:
        print(f"\nError: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
