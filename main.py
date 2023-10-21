from flask import Flask, render_template, request
from flask_cors import cross_origin
from logging.config import dictConfig

from logger import get_log_configuration
from translate import Logger, run_conversation
from sharepoint import get_files_information
from utils import extract_specific_path
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


@app.route('/ping')
def ping():
    app.logger.info('Entered GET /ping')
    return 'pong'


@app.route('/get-records', methods=['GET'])
@cross_origin()
def get_table_records():
    app.logger.info('Entered GET /get-table-records')

    table_name = 'Records'

    response = airtable_api.get_all_records_from_table(table_name)

    print("Response:", response)

    return response

@app.route('/add-record', methods=['POST'])
@cross_origin()
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
    documents = request_body["Documents"]
    added_documents_names = [document["Name"] for document in documents]
    records = airtable_api.get_all_records_from_table("Documents")
    record_names = [record["fields"]["Name"] for record in records['records']]
    record_ids_in_table = [record["id"] for record in records['records'] if record["fields"]["Name"] in added_documents_names]
    unsaved_documents = [document for document in documents if document["Name"] not in record_names]

    saved_docs_ids = []
    for unsaved_doc in unsaved_documents:
        doc_response = airtable_api.add_record("Documents", unsaved_doc)
        saved_docs_ids.append(doc_response["id"])

    record_request_body = {
        "Date": request_body["Date"],
        "Diagnosis": request_body["Diagnosis"],
        "Form": request_body["Form"],
        "Documents": record_ids_in_table + saved_docs_ids,
        "History_number": request_body["History_number"]
    }

    response = airtable_api.add_record("Records", record_request_body)

    print("Response:", response)

    return response


@app.route('/recognize', methods=['POST'])
@cross_origin()
def recognize_audio():
    app.logger.info('Entered POST /recognize')

    request_body = request.get_json()
    app.logger.info('Started agent run message %s', request_body)

    response = run_conversation(request_body, logger=FlaskLogger(app))

    print("Response:", response)

    return response

@app.route('/getFiles', methods=['GET'])
def get_sharepoint_files():
    app.logger.info('Entered GET /get-files')

    response = get_files_information()

    print("Response:", response)

    return response

@app.route('/parse-file', methods=['POST'])
def parse_file():
    extract_specific_path("./pdfs/Evolucion.pdf", "jsonForms/evolucion.json")
    return {}

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
