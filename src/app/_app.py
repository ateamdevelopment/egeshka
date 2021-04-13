from flask import Flask

__all__ = ['create_app']


def create_app():
    """
    :return: flask app with config from config.json
    """
    app = Flask('src.main')
    path_to_config = 'app/test_config.json'
    app.config.from_json(path_to_config)
    return app
