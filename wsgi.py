from application import init_app
from logging.config import dictConfig


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '%(asctime)s %(levelname)s th=%(threadName)s logger=%(name)s in %(module)s (%(filename)s#%(lineno)s '
                  'in %(funcName)s): %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',  # TODO - set to INFO by default, or DEBUG based on config (if possible)
        'handlers': ['wsgi']
    }
})

app = init_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
