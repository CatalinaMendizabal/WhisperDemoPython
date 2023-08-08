import base64
import json

import os
from flask.cli import load_dotenv
import openai

import strings
from sharepoint import get_files_information

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


def get_initial_state(input_text, form_type):
    return [
        {"role": "system", "content": strings.generic_prompt()},
        {"role": "user", "content": form_type + " " + input_text},
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
                                       "- Admisiones internación adultos"
                                       "- Evolución",
                    }
                },
                "required": ["format_name"],
            },
        },
    ]


def run_conversation(request_body, logger: Logger):
    input_text = translate_audio(request_body, logger)
    form_type = request_body['type']

    logger.info(f"Input text: {input_text}")

    messages = get_initial_state(input_text, form_type)

    # Get all the files from sharepoint
    files = get_files_information()

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

        function_response = function_to_call(form_type)

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

        logger.info("Getting files from sharepoint")
        allTheFiles = get_matching_files(second_response["choices"][0]["message"], logger)
        logger.info("Got files from sharepoint")

        final_response = {
            "response": second_response["choices"][0]["message"],
            "files": allTheFiles
        }

        return final_response


def get_specific_prompt(form_type):
    if form_type.__eq__("Epicrisis adultos y pediatria"):
        return strings.epicrisis_prompt()
    elif form_type.__eq__("Admisiones internacion adultos"):
        return strings.admissions_prompt()
    # elif form_type.__eq__("Evolucion"):
    #     return strings.admissions_prompt()
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


def get_matching_files(response, logger: Logger):
    logger.info('Entered get matching files')

    files = get_files_information()

    # Extract all words from the content in the response_template and convert them to a set
    words_in_template = set(response["content"].split())

    # Search for files that have any of the words in their name
    matching_files = []
    for file in files:
        file_name = file["name"]
        if any(word in words_in_template and len(word) > 3 for word in file_name.split()):
            matching_files.append(file)

    # Print the matching files
    for file in matching_files:
        print("Name:", file["name"])
        print("Link:", file["value"])

    return matching_files
