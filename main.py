from flask import Flask, render_template, request
from logging.config import dictConfig
from translate import translate_audio, Logger, run_conversation

# This configuration should only be used in development
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)


class FlaskLogger(Logger):
    def __init__(self, app):
        self._app = app

    def info(self, message):
        self._app.logger.info(message)

    def error(self, message):
        self._app.logger.error(message)

    def warning(self, message):
        self._app.logger.warning(message)

    def debug(self, message):
        self._app.logger.debug(message)


@app.route('/')
def voice_recognition_page():
    return render_template('index.html')


@app.route('/recognize', methods=['POST'])
def recognize_audio():
    app.logger.info('Entered POST /recognize')
    request_body = request.get_json()
    response = run_conversation(request_body, logger=FlaskLogger(app))
    # response = run_conversation(request_body, logger=FlaskLogger(app))

    return response


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
