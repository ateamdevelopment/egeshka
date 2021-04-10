from src.utils.functions import tab

from src.utils.logs.formatters._wrap_formatter import WrapFormatter

__all__ = ['ExceptFormatter']


class ExceptFormatter(WrapFormatter):
    def formatException(self, ei):
        formatted_exception = super().formatException(ei)
        return tab(
            f'<<<\n{tab(formatted_exception)}' +
            ('' if formatted_exception.endswith('\n') else '\n') +
            '>>>'
        )
