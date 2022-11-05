

def str2bool(text, test=True):
    """Test if a string 'looks' like a boolean value.
    Args:
        text: Input text
        test (default = True): Set which boolean value to look for
    Returns:
        True if the text looks like the selected boolean value
    """
    if test:
        return str(text).lower() in ['1', 'y', 'yes', 't', 'true', 'ok', 'on', ]
    else:
        return str(text).lower() in ['0', 'n', 'no', 'none', 'f', 'false', 'off', ]
    

def is_bool(text):
    """Determine if a string value 'looks' like a boolean."""
    if str2bool(text, True):
        return True
    elif str2bool(text, False):
        return True
    else:
        return False
