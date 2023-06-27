from flask import Flask, render_template, request
from logging.config import dictConfig

from logger import get_log_configuration
from translate import translate_audio, Logger, run_conversation

# This configuration should only be used in development
dictConfig(get_log_configuration())

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
