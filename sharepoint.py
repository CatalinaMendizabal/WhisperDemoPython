from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from flask.cli import load_dotenv
import os
from urllib.parse import quote


# Replace these with your SharePoint site URL, username, and password
url = "https://alumniiaeedu.sharepoint.com/sites/Tesis2023"
sharepoint_url = "https://alumniiaeedu.sharepoint.com"
load_dotenv()
username = os.getenv("SHAREPOINT_USERNAME")
password = os.getenv("SHAREPOINT_PASSWORD")

ctx_auth = AuthenticationContext(url)

if ctx_auth.acquire_token_for_user(username, password):
    ctx = ClientContext(url, ctx_auth)
else:
    print("Failed to authenticate!")
    exit()

list_name = "Documentos"  # Replace this with the name of your SharePoint document library

web = ctx.web
ctx.load(web)
ctx.execute_query()


# Function to retrieve files inside a folder and its sub_folders
def get_files_in_folder(folder):

    # Do not retrieve files inside the "Forms" folder
    if folder.properties["Name"] == "Forms":
        return

    # Get all files inside the current folder
    folder_files = folder.files
    ctx.load(folder_files)
    ctx.execute_query()

    # Print the names and URL links of files inside the folder
    for file in folder_files:
        file_name = file.properties["Name"]
        file_url = file.properties["ServerRelativeUrl"]
        full_file_url = f"{sharepoint_url}{file_url}"

        # Get the sharing link URL
        print("File:", file_name)
        print("File URL:", full_file_url)
        print("File URL link:", quote(full_file_url, safe=':/'))

    # Get all sub_folders inside the current folder
    sub_folders = folder.folders
    ctx.load(sub_folders)
    ctx.execute_query()

    # Recursively call the function for each sub_folder
    for sub_folder in sub_folders:
        get_files_in_folder(sub_folder)


# Get the list (library) object
list_obj = web.lists.get_by_title(list_name)
ctx.load(list_obj)
ctx.execute_query()

# Get the root folder of the list
root_folder = list_obj.root_folder
ctx.load(root_folder)
ctx.execute_query()

# Call the function to retrieve files in the root folder and its sub_folders
get_files_in_folder(root_folder)
