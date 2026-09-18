MAX_OUTPUT_CHARACTERS = 4000

def truncate_output(text: str, max_char : int = MAX_OUTPUT_CHARACTERS) -> str:
    """ Truncates output to first 1500 char last 2500 char if too long"""

    if len(text) <= max_char:
        return text

    head_len = 1500
    tail_len = 2500

    return (
        text[:head_len]
        + "\n\n[Output truncated]\n\n"
        + text[-tail_len:]
    )