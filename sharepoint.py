from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from flask.cli import load_dotenv
import os

# Replace these with your SharePoint site URL, username, and password
site_url = "https://alumniiaeedu.sharepoint.com/sites/Tesis2023"
load_dotenv()
username = os.getenv("SHAREPOINT_USERNAME")
password = os.getenv("SHAREPOINT_PASSWORD")

ctx_auth = AuthenticationContext(site_url)

if ctx_auth.acquire_token_for_user(username, password):
    ctx = ClientContext(site_url, ctx_auth)
else:
    print("Failed to authenticate!")
    exit()

list_name = "Adultos"  # Replace this with the name of your SharePoint document library

web = ctx.web
ctx.load(web)
error = "'NoneType' object has no attribute 'replace'"
ctx.execute_query()

list_obj = web.lists.get_by_title(list_name)
ctx.load(list_obj)
ctx.execute_query()

# Retrieve all items (documents) from the list
items = list_obj.items
ctx.load(items)
ctx.execute_query()

for item in items:
    # Print the name of the document (file)
    print(item.properties["FileLeafRef"])
