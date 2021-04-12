from logging import info

from src.app import app
from src.urls import init_urls
from src.utils.logs import init_loggers
from src._backup import init_backup

init_loggers()
init_urls(app)
init_backup()

info('Server started !')

if __name__ == '__main__':
    app.run(threaded=True)
