import tkinter as tk
import os
from notion_client import Client
from pprint import pprint
# # Create a new Notion API client
# notion = Client(auth="secret_Rs800ockGMwCwW6w7SY34v9m2QXtFCkeuqleS77U8Pb")

# # Get the database ID of the database you want to retrieve data from
# database_id = "614f2195f4ee4c9b8db9b232b8d53948"


notion = Client(
    auth="secret_Rs800ockGMwCwW6w7SY34v9m2QXtFCkeuqleS77U8Pb")
database_id = "614f2195f4ee4c9b8db9b232b8d53948"

results = notion.databases.query(
    **{
        "database_id": database_id,
        "sorts": [{"property": "Created time", "direction": "descending"}],
    }
).get("results")

if len(results) > 0:
    first_result = results[0]
    properties = first_result["properties"]
    if "Project" in properties:
        project = properties["Project"]["title"][0]["rich_text"]["content"]
        print("Project:", project)
    else:
        print("No project found in properties.")
else:
    print("No results found in database.")
