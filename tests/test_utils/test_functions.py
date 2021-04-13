import re

from tests.conftest import parameterize
from src.utils.functions import generate_random_token, file_line_count


@parameterize('length', (30, 50, 100))
def test_generate_random_token(length):
    assert re.match(
        f'^.{{{length}}}$',
        generate_random_token(length)
    )


@parameterize('number_lines', (0, 1, 100, 1000, 10000))
def test_file_line_count(temp_text_file, number_lines):
    temp_text_file.write('\n'.join([f'line: {i}' for i in range(number_lines)]))
    assert file_line_count(temp_text_file) == number_lines
