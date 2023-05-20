from flask import Flask, render_template, request
import whisper

app = Flask(__name__)
model = whisper.load_model("base")


@app.route('/')
def voice_recognition_page():
    return render_template('index.html')


@app.route('/recognize', methods=['POST'])
def recognize_audio():
    # Get the audio file from the POST request

    audio_requested = request.files['audio']
    audio_path = audio_requested.filename
    print(audio_path)
    # save the audio file temporarily
    audio_requested.save('aux.' + audio_path)

    result = model.transcribe('aux.' + audio_path)
    print(result)

    # audio = request.files['audio']
    # audio.save('audio.wav')  # Save the audio file temporarily

    # Perform voice recognition using Whisper
    # recognized_text = whisper.recognize('audio.wav')

    # Remove the temporary audio file
    # You may want to handle this differently in a production environment
    # os.remove('audio.wav')

    # return recognized_text
    return result["text"]


if __name__ == '__main__':
    app.run()
