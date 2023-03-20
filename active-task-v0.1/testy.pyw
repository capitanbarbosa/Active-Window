import tkinter as tk
from tkinter import ttk
import requests
import json
import time
import threading
from notion_client import Client
import pprint

# Set your Notion API integration token
integration_token = 'secret_Rs800ockGMwCwW6w7SY34v9m2QXtFCkeuqleS77U8Pb'
databaseId = '614f2195f4ee4c9b8db9b232b8d53948'
notion_log = Client(auth=integration_token)

# Create a list to store the results from the log database
results = []
name = ''
note = ''


headers = {
    "Authorization": "Bearer " + integration_token,
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}


# Initialize the current index to 0
current_index = 0

# -> Notion-client actions for Projects database
# Authenticate with Notion API using integration token
notion_projects = Client(auth=integration_token)
# Dummy data for the dropdown menu
projects = [{"name": "Project A", "status": "Active"},    {"name": "Project B", "status": "Active"},    {
    "name": "Project C", "status": "Inactive"},    {"name": "Project D", "status": "Complete"}]

# Projects database
database_id = "ef5fcadfa8144d22b2d613a5c86b9cf6"
results = notion_projects.databases.query(database_id).get("results")
print(results)
# Get the Name column contents
projects = ['']+[page['properties']['Name']['title']
                 [0]['text']['content'] for page in results]
projects.sort()
# Print the projects arraylist
# pprint.pprint(projects)
current_project = ""

# -> Notion-client actions for Projects database
#


# def readDatabase(databaseId):
#     database = notion_log.databases.retrieve(database_id=databaseId)

#     results = []
#     for page in notion_log.databases.query(
#             **{
#                 "database_id": databaseId,
#             }
#     ).get("results"):
#         name = page.properties["Name"].title[0].plain_text
#         note = page.properties["Note"].rich_text[0].plain_text if len(
#             page.properties["Note"].rich_text) > 0 else ""
#         page_id = page.id
#         active = page.properties["Active?"].checkbox
#         current_project = page.properties["Project"].rich_text[0].plain_text if len(
#             page.properties["Project"].rich_text) > 0 else ""
#         results.append((name, note, page_id, active))

#     # Set the state of the tkinter Checkbox widget to match the "Active?" column value of the current page
#     checkbox.var.set(results[current_index][3])

#     # print(f"Results: {results}")
#     show_result(current_index, project)
