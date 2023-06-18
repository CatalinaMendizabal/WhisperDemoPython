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
    # get the request body
    body = request.get_json()

    # get the audio data and sample rate from the request
    audio_data = base64.b64decode(body['audio'])

    # save the audio data to a file
    with open('audio-temp.m4a', 'wb') as f:
        f.write(audio_data)

    # load the model and transcribe the audio
    # model = openai.Completion.create(
    #     engine="davinci",
    #     prompt="This is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: I'd like to book a flight to Cairo.\nAI:",
    #     temperature=0.9,
    #     max_tokens=150,
    #     top_p=1,
    #     frequency_penalty=0.0,
    #     presence_penalty=0.6,
    #     stop=["\n", " Human:", " AI:"]
    # )
    # sin openai --> model = whisper.load_model("base")

    # load the audio
    # sin openai --> audio = whisper.load_audio("audio-temp.m4a")
    audio_file = open("audio-temp.m4a", "rb")
    result = openai.Audio.translate("whisper-1", audio_file)

    # transcribe audio
    # result = model.transcribe(audio)

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