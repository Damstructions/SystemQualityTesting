import re
from decimal import Decimal


def money(text):
    """First number in a string as a Decimal: '$360 *includes tax' -> 360."""
    m = re.search(r"\d[\d,]*(?:\.\d+)?", text or "")
    return Decimal(m.group().replace(",", "")) if m else Decimal(0)


def exact(text):
    """Regex that matches a whole string, ignoring surrounding whitespace."""
    return re.compile(rf"^\s*{re.escape(text)}\s*$")
