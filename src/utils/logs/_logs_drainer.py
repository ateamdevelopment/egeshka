import atexit
from datetime import datetime
from logging import info
from threading import Thread
from time import sleep
from typing import Final

import src.utils as utils
from src.utils.functions import file_line_count

__all__ = ['LogsDrainer']


class LogsDrainer:
    DEFAULT_DELAY: Final[int] = 60  # seconds
    DEFAULT_MAX_LINE_COUNT: Final[int] = 1000
    DEFAULT_DIRECTORY_TO_UPLOAD: Final[str] = '/logs'

    def __init__(
            self,
            path_to_logs: str,
            delay: int = DEFAULT_DELAY,
            max_line_count: int = DEFAULT_MAX_LINE_COUNT,
            directory_to_upload: str = DEFAULT_DIRECTORY_TO_UPLOAD
    ):
        """
        :param path_to_logs: absolute path (from /src) to the logs file
            (including the filename)
        :param delay: the delay between checks the length of the logs file in seconds
        :param max_line_count: the number of lines at which the file is loaded to the
            file database and cleared
        :param directory_to_upload: directory on the file base for uploading logs
            (the file name is generated automatically as the current time)
        """
        self._path_to_logs: Final[str] = path_to_logs
        self._delay: Final[int] = delay
        self._max_line_count: Final[int] = max_line_count
        self._directory_to_upload: Final[str] = directory_to_upload

    def listen(self) -> None:
        def _listen():
            info(f'{self.__class__.__name__} started listening the logs')
            while True:
                sleep(self._delay)
                with open(self._path_to_logs, 'r') as logs_file_r:
                    logs_line_count = file_line_count(logs_file_r)

                if logs_line_count >= self._max_line_count:
                    self._upload_logs()
                    open(self._path_to_logs, 'w').close()  # clear logs file

        Thread(target=_listen, daemon=True).start()
        atexit.register(self._upload_logs)

    @property
    def _path_to_upload(self) -> str:
        return f'{self._directory_to_upload}/' \
               f'{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.log'

    def _upload_logs(self) -> None:
        with open(self._path_to_logs, 'rb') as logs_file_rb:
            utils.file_base.upload(
                logs_file_rb,
                self._path_to_upload
            )
