from dotenv import load_dotenv

import os
import requests

load_dotenv()

api_key = os.getenv('AIRTABLE_API_KEY')
base_id = os.getenv('BASE_ID')
base_url = "https://api.airtable.com/v0"
headers = {"Authorization": f"Bearer {api_key}"}


def get_tables():
    url = f"{base_url}/meta/bases/{base_id}/tables"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.status_code}")


def add_record(table_name, fields):
    url = f"{base_url}/{base_id}/{table_name}"
    response = requests.post(url, headers=headers, json={"fields": fields})

    print(response.text)
    print(response.content)
    if response.status_code == 200:
        return response.json()
    return f"Error adding record to table: {response.text}"


def get_all_records_from_table(table_name):
    url = f"{base_url}/{base_id}/{table_name}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def get_all_by_table_name(table_name):
    url = f"{base_url}/{base_id}/{table_name}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def get_table_by_name(table_name):
    print(base_url)
    print(base_id)
    url = f"{base_url}/meta/bases/{base_id}/tables/{table_name}"
    response = requests.patch(url, headers=headers, json={"name": table_name})
    if response.status_code == 200:
        return response.json()
    return None


def get_fields_from_table(table_name):
    table = get_table_by_name(table_name)
    fields = table['fields']
    for field in fields:
        print(field['name'])
        print(field['id'])

    # return fields['name']
