import base64
import json

import os
from flask.cli import load_dotenv
import openai

import strings

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class Logger:
    def info(self, message):
        print(message)

    def error(self, message):
        print(message)

    def warning(self, message):
        print(message)

    def debug(self, message):
        print(message)


def get_initial_state(input_text):
    return [
        {"role": "system", "content": strings.generic_prompt()},
        {"role": "user", "content": input_text},
    ]


def get_functions():
    return [
        {
            "name": strings.GET_SPECIFIC_PROMPT,
            "description": strings.GET_SPECIFIC_PROMPT_DESCRIPTION,
            "parameters": {
                "type": "object",
                "properties": {
                    "format_name": {
                        "type": "string",
                        "description": "Nombre del formato que el usuario quiere obtener. Estos pueden ser:"
                                       "- Epicrisis adultos y pediatría"
                                       "- Admisiones internación adultos",
                    }
                },
                "required": ["format_name"],
            },
        },
    ]


def run_conversation(request_body, logger: Logger):
    input_text = translate_audio(request_body, logger)

    # input_text = "Formulario de Epicrisis adultos y pediatría para el paciente Tomas Ignacio Berretta, masculino, " \
    #                  "de 5 años de edad, con diagnóstico de COVID-19. Ingresó en el día de hoy a las 10:00 hs. "

    logger.info(f"Input text: {input_text}")

    messages = get_initial_state(input_text)

    response = openai.ChatCompletion.create(
        model=os.getenv("MODEL_NAME"),
        messages=messages,
        functions=get_functions(),
        function_call="auto",  # auto is default, but we'll be explicit
    )

    response_message = response["choices"][0]["message"]
    logger.info(f"Response message: {response_message}")

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            strings.GET_SPECIFIC_PROMPT: get_specific_prompt,
        }

        # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])

        function_response = function_to_call(
            format_name=function_args.get("format_name"),
        )

        if function_response is None:
            function_response = "No se encontró el formato solicitado"

        # Step 4: send the info on the function call and function response to GPT
        messages.append({
            "role": "function",
            "name": function_name,
            "content": function_response,
        })  # extend conversation with function response

        messages.append({
            "role": "system",
            "content": function_response,
        })

        second_response = openai.ChatCompletion.create(
            model=os.getenv("MODEL_NAME"),
            messages=messages,
        )

        logger.info(f"Second response: {second_response}")

        # get a new response from GPT where it can see the function response
        return second_response["choices"][0]["message"]


def get_specific_prompt(format_name):
    if format_name == "Epicrisis adultos y pediatría":
        return strings.epicrisis_adultos_y_pediatria()
    elif format_name == "Admisiones internación adultos":
        return strings.admisiones_internacion_adultos()
    else:
        return "No se encontró el formato solicitado"


def translate_audio(request_body, logger: Logger):
    logger.info("Entered translate_audio")
    # get the audio data and sample rate from the request
    audio_data = base64.b64decode(request_body['audio'])

    # save the audio data to a file
    with open('tmp/audio-temp.m4a', 'wb') as f:
        f.write(audio_data)

    # load the audio
    audio_file = open("tmp/audio-temp.m4a", "rb")

    logger.info("Calling OpenAI API")
    result = openai.Audio.transcribe("whisper-1", audio_file)

    # get the transcription
    transcription = result["text"]

    logger.info(f"Whisper response: {str(transcription)}")

    # delete the temporary audio file
    os.remove('tmp/audio-temp.m4a')

    return transcription
