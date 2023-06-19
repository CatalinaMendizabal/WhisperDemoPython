import base64

from flask import Flask, render_template, request
import os
from flask.cli import load_dotenv
import openai

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route('/')
def voice_recognition_page():
    return render_template('index.html')


@app.route('/recognize', methods=['POST'])
def recognize_audio():
    body = request.get_json()

    # get the audio data and sample rate from the request
    audio_data = base64.b64decode(body['audio'])

    # save the audio data to a file
    with open('tmp/audio-temp.m4a', 'wb') as f:
        f.write(audio_data)

    # load the audio
    audio_file = open("tmp/audio-temp.m4a", "rb")

    # transcribe audio to spanish
    result = openai.Audio.translate("whisper-1", audio_file)

    # get the transcription
    transcription = result["text"]

    # prepare the JSON response
    response_data = {
        'action': 'transcription',
        'transcription': transcription
    }

    # delete the temporary audio file
    os.remove('tmp/audio-temp.m4a')

    return response_data


# make function to run agent with openai and


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
