import asyncio
import websockets
import base64
import requests
import whisper


async def translate_audio(websocket):
    async for message in websocket:
        # Decode the base64 input
        audio_data = base64.b64decode(message)

        # Save the audio data to a file (optional)
        with open('audio.m4a', 'wb') as audio_file:
            audio_file.write(audio_data)

        # Perform voice recognition using Whisper
        model = whisper.load_model("base")
        result = model.transcribe("audio.m4a")

        transcription = result["text"]

        # Prepare the JSON response
        response_data = {
            'action': 'transcription',
            'transcription': transcription
        }

        # Send the JSON response back to the client
        await websocket.send(str(response_data))


start_server = websockets.serve(translate_audio, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

