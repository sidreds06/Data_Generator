"""
Rule parser module for parsing rule strings from Excel template.
"""


def parse_rule(rule):
    """
    Parse a rule string into a dictionary of parameters.

    Format: parameter1:value1; parameter2:value2; parameter3:value3

    Args:
        rule (str): Rule string to parse

    Returns:
        dict: Dictionary of parameter names to values

    Example:
        >>> parse_rule("type:integer; range:1000-9999; unique:true")
        {'type': 'integer', 'range': '1000-9999', 'unique': 'true'}
    """
    if not rule or not isinstance(rule, str):
        return {}

    parts = [p.strip() for p in rule.split(';')]
    params = {}

    for p in parts:
        if ':' in p:
            key, value = p.split(':', 1)
            params[key.strip()] = value.strip()

    return params


def validate_rule(params):
    """
    Validate that a rule has required parameters for its type.

    Args:
        params (dict): Parsed rule parameters

    Returns:
        tuple: (is_valid, error_message)
    """
    data_type = params.get("type")

    if not data_type:
        return False, "Rule must specify 'type' parameter"

    # Type-specific validation
    validations = {
        "integer": lambda p: "range" in p,
        "decimal": lambda p: "range" in p,
        "string": lambda p: "pattern" in p,
        "choice": lambda p: "values" in p,
        "date": lambda p: "start" in p and "end" in p,
        "datetime": lambda p: "start" in p and "end" in p,
    }

    if data_type in validations:
        if not validations[data_type](params):
            return False, f"Type '{data_type}' is missing required parameters"

    return True, ""
