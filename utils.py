import json

import PyPDF2


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        pdf_text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()
    return pdf_text


def parse_text_to_json(pdf_text):
    # Here, you need to define your parsing logic based on the structure of your PDF.
    # For this example, I'll assume that the PDF text contains lines with "key: value" format.
    data = {}
    lines = pdf_text.split('-')
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)  # Split at the first occurrence of ":"
            data[key.strip()] = value.strip()
    return data


def extract_specific_path(path, file_name):
    extracted_text = extract_text_from_pdf(path)
    parsed_data = parse_text_to_json(extracted_text)

    # Save the JSON data to a file
    with open(file_name, "w") as json_file:
        json.dump(parsed_data, json_file, indent=4)