import logging
from logging.config import dictConfig

from application import init_app


class Ignore200sFilter(logging.Filter):
    def filter(self, record):
        do_not_show = [
            ' /state HTTP/1.1" 200 ',
            ' /task_queue HTTP/1.1" 200 ',
            ' /measurement HTTP/1.1" 200 ',
            ' /routine HTTP/1.1" 200 ',
            ' /meta_state HTTP/1.1" 200 ',
            ' /state HTTP/1.1" 200 ',
        ]
        return all([elem not in record.getMessage() for elem in do_not_show])


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '%(asctime)s %(levelname)s th=%(threadName)s logger=%(name)s in %(module)s (%(filename)s#%(lineno)s '
                  'in %(funcName)s): %(message)s',
    }},
    'filters': {'ignore_200s': {
        '()': Ignore200sFilter,
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default',
        'filters': ['ignore_200s']
    }},
    'root': {
        'level': 'DEBUG',  # TODO - set to INFO by default, or DEBUG based on config (if possible)
        'handlers': ['wsgi']
    }
})

app = init_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
