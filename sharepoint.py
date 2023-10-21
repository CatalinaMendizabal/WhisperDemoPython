from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from flask.cli import load_dotenv
import os
from urllib.parse import quote

load_dotenv()
username = os.getenv("SHAREPOINT_USERNAME")
password = os.getenv("SHAREPOINT_PASSWORD")
url = os.getenv("SHAREPOINT_LONG_URL")
sharepoint_url = os.getenv("SHAREPOINT_URL")


def get_files_information():
    # Replace these with your SharePoint site URL, username, and password

    ctx_auth = AuthenticationContext(url)

    if ctx_auth.acquire_token_for_user(username, password):
        ctx = ClientContext(url, ctx_auth)
    else:
        print("Failed to authenticate!")
        exit()

    list_name = "Guía de Práctica Clínica"

    web = ctx.web
    ctx.load(web)
    ctx.execute_query()

    # Get the list (library) object
    list_obj = web.lists.get_by_title(list_name)
    ctx.load(list_obj)
    ctx.execute_query()

    # Get the root folder of the list
    root_folder = list_obj.root_folder
    ctx.load(root_folder)
    ctx.execute_query()

    # Call the function to retrieve files in the root folder and its sub_folders
    file_info = get_files_in_folder(root_folder, ctx)

    # Print the results
    for file in file_info:
        print(f"Name: {file['name']}")
        print(f"Link: {file['value']}")
        print()

    return file_info


def get_files_in_folder(folder, ctx):
    results = []

    # Do not retrieve files inside the "Forms" folder
    if folder.properties["Name"] == "Forms":
        return results

    # Get all files inside the current folder
    folder_files = folder.files

    ctx.load(folder_files)
    ctx.execute_query()

    # Return the names and URL links of files inside the folder
    for file in folder_files:
        f_name = file.properties["Name"]
        file_url = file.properties["ServerRelativeUrl"]
        full_file_url = f"{sharepoint_url}{file_url}"
        file_link = quote(full_file_url, safe=':/')

        # Append the f_name and file_link to the results list
        results.append({"name": f_name, "value": file_link})

    # Get all sub_folders inside the current folder
    sub_folders = folder.folders
    ctx.load(sub_folders)
    ctx.execute_query()

    # Recursively call the function for each sub_folder
    for sub_folder in sub_folders:
        results.extend(get_files_in_folder(sub_folder, ctx))

    return results
