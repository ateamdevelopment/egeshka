import random
import string
from typing import TextIO

__all__ = ['generate_random_token', 'file_line_count', 'tab']


_LETTERS = string.ascii_lowercase + string.ascii_uppercase + string.digits


def generate_random_token(length: int) -> str:
    """
    :return: string consisting of a random set [a-zA-Z0-9]
    """
    return ''.join(random.choice(_LETTERS) for _ in range(length))


def file_line_count(file: TextIO) -> int:
    """
    :param file: file is opened in 'r' mode
    :return: number of lines in file
    """
    file.seek(0)
    line_count = -1
    for last_line, _ in enumerate(file):
        line_count = last_line
    return line_count + 1


def tab(text: str) -> str:
    """
    :return: source text with all tabulated lines
    """
    if text.endswith('\n'):
        return '\t' + text.replace('\n', '\n\t')[:-1]
    return '\t' + text.replace('\n', '\n\t')
