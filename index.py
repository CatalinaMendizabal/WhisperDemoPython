import base64

from flask import Flask, render_template, request
import whisper
import os

app = Flask(__name__)


@app.route('/')
def voice_recognition_page():
    return render_template('index.html')


@app.route('/recognize', methods=['POST'])
def recognize_audio():
    # get the request body
    body = request.get_json()

    # get the audio data and sample rate from the request
    audio_data = base64.b64decode(body['audio'])

    # save the audio data to a file
    with open('audio-temp.m4a', 'wb') as f:
        f.write(audio_data)

    # load the model
    model = whisper.load_model("base")

    # load the audio
    audio = whisper.load_audio("audio-temp.m4a")

    # transcribe audio
    result = model.transcribe(audio)

    # get the transcription
    transcription = result["text"]

    # prepare the JSON response
    response_data = {
        'action': 'transcription',
        'transcription': transcription
    }

    # delete the temporary audio file
    os.remove('audio-temp.m4a')

    # return the recognized text
    return response_data


if __name__ == '__main__':
    app.run(host='localhost', port=8080)