from typing import Final

from flask import Flask

from src.app._app import create_app

__all__ = ['app']

app: Final[Flask] = create_app()
