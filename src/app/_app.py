import os

from flask import Flask

from src import ON_HOSTING

__all__ = ['create_app']


def create_app():
    """
    :return: flask app with config from dev_config.json or prod_config.json
    """
    app = Flask('src.main')
    path_to_config = f'app/{"prod" if ON_HOSTING else "dev"}_config.json'
    app.config.from_json(path_to_config)
    return app
