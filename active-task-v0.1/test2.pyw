from notion_client import Client

# Set your Notion API integration token
integration_token = 'secret_Rs800ockGMwCwW6w7SY34v9m2QXtFCkeuqleS77U8Pb'
database_id = '614f2195f4ee4c9b8db9b232b8d53948'

# Authenticate with Notion API using integration token
notion = Client(auth=integration_token)

# Query the database and get the results
results = notion.databases.query(database_id).get("results")

# Loop through the list of results
for result in results:
    # Get the Name value for the current result, if it exists
    name = ""
    if "Name" in result["properties"] and len(result["properties"]["Name"]["title"]) > 0:
        name = result["properties"]["Name"]["title"][0]["text"]["content"]

    # Get the Note value for the current result, if it exists
    note = ""
    if "Note" in result["properties"] and len(result["properties"]["Note"]["rich_text"]) > 0:
        note = result["properties"]["Note"]["rich_text"][0]["text"]["content"]

    # Get the Active? value for the current result, if it exists
    active = False
    if "Active?" in result["properties"] and result["properties"]["Active?"]["checkbox"]:
        active = result["properties"]["Active?"]["checkbox"]

    # Get the Project value for the current result, if it exists
    project = ""
    if "Project" in result["properties"] and len(result["properties"]["Project"]["rich_text"]) > 0:
        project = result["properties"]["Project"]["rich_text"][0]["plain_text"]

    # Print the Name, Note, Active?, and Project values for the current result
    print("Name:", name)
    print("Note:", note)
    print("Active?:", active)
    print("Project:", project)

# Set the state of the tkinter Checkbox widget to match the "Active?" column value of the current page
checkbox.var.set(results[current_index][3])

# print(f"Results: {results}")
show_result(current_index, project)
