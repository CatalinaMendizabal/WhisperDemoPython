from flask import Flask, render_template, request
from logging.config import dictConfig

from logger import get_log_configuration
from translate import Logger, run_conversation
import airtable_api

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


@app.route('/get-records', methods=['GET'])
def get_table_records():
    app.logger.info('Entered GET /get-table-records')

    table_name = 'Records'

    response = airtable_api.get_all_records_from_table(table_name)

    print("Response:", response)

    return response


@app.route('/add-record', methods=['POST'])
def add_record():
    app.logger.info('Entered POST /add-record')

    request_body = request.get_json()
    app.logger.info('Started agent run message %s', request_body)

    # mock_fields = {
    #     "Date": "2021-05-06",
    #     "Diagnosis": "Diagnosis del paciente",
    #     "Documents": [{"url": "https://www.google.com"}, {
    #         "url": "https://airtable.com/app8r9i9DgtZAtU9l/tblSId1c58UtaXsvQ/viwVrQcujfC2VJRHP?blocks=hide"}],
    #     "Form": "Ingreso",
    # }

    response = airtable_api.add_record("Records", request_body)

    print("Response:", response)

    return response


@app.route('/recognize', methods=['POST'])
def recognize_audio():
    app.logger.info('Entered POST /recognize')

    request_body = request.get_json()
    app.logger.info('Started agent run message %s', request_body)

    response = run_conversation(request_body, logger=FlaskLogger(app))

    print("Response:", response)

    return response


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
