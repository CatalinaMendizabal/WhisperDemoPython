from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from flask.cli import load_dotenv
import os

from office365.sharepoint.listitems.caml.query import CamlQuery

# Replace these with your SharePoint site URL, username, and password
url = "https://alumniiaeedu.sharepoint.com/sites/Tesis2023"
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
folder_name = "Adultos"  # Replace this with the name of the folder

web = ctx.web
ctx.load(web)
ctx.execute_query()

# Get the folder from the document library
list_obj = web.lists.get_by_title(list_name)
folder = list_obj.root_folder.folders.get_by_url(folder_name)
ctx.load(folder)
ctx.execute_query()

# Retrieve all items (documents) from the folder
query = CamlQuery.create_all_items_query()
items = folder.files
ctx.load(items)
ctx.execute_query()

for item in items:
    # Print the name of the document (file) in the folder
    print(item.properties["Name"])