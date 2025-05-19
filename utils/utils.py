import re


def sanitize_sheet_name(name):
    """
    Sanitizes a string to be a valid Excel sheet name.
    Excel sheet names cannot contain: / \ ? * [ ] :
    They also have a maximum length of 31 characters.
    """
    # Remove invalid characters
    name = re.sub(r"[\\/\?\*\[\]:]", "", name)
    # Truncate to 31 characters
    return name[:31]
