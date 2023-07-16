import json

GET_SPECIFIC_PROMPT = 'get_specific_prompt'
GET_SPECIFIC_PROMPT_DESCRIPTION = 'Obtener un formato específico'


# def epicrisis_adultos_y_pediatria():
#     return """Epicrisis adultos y pediatría
#     Nombre del paciente: Nombre del paciente mencionado en el mensaje
#     Edad: Edad del paciente mencionado en el mensaje
#     Sexo: Sexo del paciente mencionado en el mensaje
#     Fecha de ingreso: Fecha de ingreso del paciente mencionado en el mensaje
#     """
#
#
# def admisiones_internacion_adultos():
#     return """Admisiones internacion adultos
#     \nNombre del paciente: Nombre del paciente mencionado en el mensaje
#     \nEdad: Edad del paciente mencionado en el mensaje
#     \nSexo: Sexo del paciente mencionado en el mensaje
#     \nFecha de ingreso: Fecha de ingreso del paciente mencionado en el mensaje
#     \nFecha de egreso: Fecha de egreso del paciente mencionado en el mensaje
#     \nMotivo de admisiOn: Motivo de admisiOn del paciente mencionado en el mensaje
#     \nDiagnostico principal: DiagnOstico principal del paciente mencionado en el mensaje
#     \nMedicacion: Medicacion asignada para el paciente mencionado en el mensaje
#     """


def admissions_prompt():
    json_path = "jsonForms/admisiones.json"

    with open(json_path, 'r') as file:
        translations = json.load(file)

    return "\n".join([f"{key}: {value}" for key, value in translations.items()])


def epicrisis_prompt():
    json_path = "jsonForms/epicrisis.json"

    with open(json_path, 'r') as file:
        translations = json.load(file)

    return "\n".join([f"{key}: {value}" for key, value in translations.items()])


def evolution_prompt():
    json_path = "jsonForms/evolucion.json"

    with open(json_path, 'r') as file:
        translations = json.load(file)

    return "\n".join([f"{key}: {value}" for key, value in translations.items()])


def generic_prompt():
    return f"""Ten en cuenta las siguientes especificaciones:
        - Eres un asistente de medicina virtual. La forma en que funciona es que el usuario tiene un formato especifico
        de formulario que debe llenar para guardar la información de un paciente. La interaccion comienza cuando el 
        usuario te envia un mensaje de voz con la información del paciente. Tu primer tarea es buscar el formulario 
        especifico que debe completar utilizando la siguiente funcion {GET_SPECIFIC_PROMPT}. Luego, tu segunda tarea es 
        completar el formulario con la información.
        
        - Los campos que no fueron mencionados o especificados dejarlos vacios
        """
