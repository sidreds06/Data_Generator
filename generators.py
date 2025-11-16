"""
Data generators for different data types.
Each generator function takes params dict and n (number of rows) and returns a list.
"""
import random
from faker import Faker

fake = Faker()


def generate_integer(params, n):
    """Generate integer values with optional unique constraint."""
    min_val, max_val = map(int, params.get("range", "0-100").split("-"))
    unique = params.get("unique", "false").lower() == "true"

    if unique:
        vals = set()
        data = []
        attempts = 0
        max_attempts = n * 10

        while len(data) < n and attempts < max_attempts:
            v = random.randint(min_val, max_val)
            if v not in vals:
                vals.add(v)
                data.append(v)
            attempts += 1

        if len(data) < n:
            raise ValueError(f"Cannot generate {n} unique integers in range {min_val}-{max_val}")
        return data
    else:
        return [random.randint(min_val, max_val) for _ in range(n)]


def generate_decimal(params, n):
    """Generate decimal/float values with specified precision."""
    min_val, max_val = map(float, params.get("range", "0.0-100.0").split("-"))
    precision = int(params.get("precision", "2"))
    return [round(random.uniform(min_val, max_val), precision) for _ in range(n)]


def generate_string(params, n):
    """Generate string values based on pattern."""
    def random_from_pattern(pattern):
        out = []
        for c in pattern:
            if c == "#":
                out.append(str(random.randint(0, 9)))
            elif c == "@":
                out.append(chr(random.randint(65, 90)))  # A-Z
            elif c == "?":
                out.append(chr(random.randint(97, 122)))  # a-z
            elif c == "*":
                choice = random.choice([
                    str(random.randint(0, 9)),
                    chr(random.randint(65, 90)),
                    chr(random.randint(97, 122))
                ])
                out.append(choice)
            else:
                out.append(c)
        return ''.join(out)

    pattern = params.get("pattern", "####")
    unique = params.get("unique", "false").lower() == "true"

    if unique:
        vals = set()
        data = []
        attempts = 0
        max_attempts = n * 10

        while len(data) < n and attempts < max_attempts:
            s = random_from_pattern(pattern)
            if s not in vals:
                vals.add(s)
                data.append(s)
            attempts += 1

        if len(data) < n:
            raise ValueError(f"Cannot generate {n} unique strings with pattern {pattern}")
        return data
    else:
        return [random_from_pattern(pattern) for _ in range(n)]


def generate_choice(params, n):
    """Generate values from a predefined list of choices."""
    choices = [x.strip() for x in params.get("values", "").split(",")]
    if not choices or choices == ['']:
        raise ValueError("Choice type requires 'values' parameter")
    return [random.choice(choices) for _ in range(n)]


def generate_boolean(params, n):
    """Generate boolean True/False values."""
    return [random.choice([True, False]) for _ in range(n)]


def generate_text(params, n):
    """Generate text sentences with specified word count."""
    word_range = params.get("words", "5-10")
    word_min, word_max = map(int, word_range.split("-"))
    return [fake.sentence(nb_words=random.randint(word_min, word_max)) for _ in range(n)]


def generate_first_name(params, n):
    """Generate realistic first names."""
    return [fake.first_name() for _ in range(n)]


def generate_last_name(params, n):
    """Generate realistic last names."""
    return [fake.last_name() for _ in range(n)]


def generate_email(params, n):
    """Generate email addresses with optional custom domain."""
    domain = params.get("domain", "example.com")
    return [f"{fake.first_name().lower()}.{fake.last_name().lower()}@{domain}" for _ in range(n)]


def generate_phone(params, n):
    """Generate phone numbers based on format pattern."""
    fmt = params.get("format", "###-###-####")

    def format_phone():
        result = []
        for c in fmt:
            if c == "#":
                result.append(str(random.randint(0, 9)))
            else:
                result.append(c)
        return ''.join(result)

    return [format_phone() for _ in range(n)]


def generate_date(params, n):
    """Generate dates within specified range."""
    import pandas as pd

    start = params.get("start", "2000-01-01")
    end = params.get("end", "2020-12-31")
    out_fmt = params.get("format", "%Y-%m-%d")

    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)

    return [fake.date_between(start_date=start_date, end_date=end_date).strftime(out_fmt) 
            for _ in range(n)]


def generate_datetime(params, n):
    """Generate datetime values within specified range."""
    import pandas as pd

    start = params.get("start", "2020-01-01")
    end = params.get("end", "2024-12-31")
    out_fmt = params.get("format", "%Y-%m-%d %H:%M:%S")

    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)

    return [fake.date_time_between(start_date=start_date, end_date=end_date).strftime(out_fmt) 
            for _ in range(n)]


def generate_address(params, n):
    """Generate realistic street addresses."""
    return [fake.address().replace("\n", ", ") for _ in range(n)]


def generate_postal_code(params, n):
    """Generate postal codes for specified country."""
    country = params.get("country", "US")

    # Map common country codes to Faker locales
    locale_map = {
        "US": "en_US",
        "CA": "en_CA",
        "UK": "en_GB",
        "GB": "en_GB",
        "FR": "fr_FR",
        "DE": "de_DE",
        "IT": "it_IT",
        "ES": "es_ES",
        "AU": "en_AU",
        "IN": "en_IN",
    }

    locale = locale_map.get(country.upper(), "en_US")
    fake_local = Faker(locale)

    return [fake_local.postcode() for _ in range(n)]
