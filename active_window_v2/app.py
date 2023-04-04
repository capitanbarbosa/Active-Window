
from notion_client import Client
from controller import *
from view import *
# from model import *


# ----------------------- DATA STRUCTURE - MODEL ---------------------
#

token = 'secret_Rs800ockGMwCwW6w7SY34v9m2QXtFCkeuqleS77U8Pb'
# Set your Notion API integration token
integration_token = 'secret_Rs800ockGMwCwW6w7SY34v9m2QXtFCkeuqleS77U8Pb'
databaseId = '614f2195f4ee4c9b8db9b232b8d53948'
name = ''
note = ''
headers = {
    "Authorization": "Bearer " + token,
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"

}
# Create a list to store the results from the database
results = []
# Initialize the current index to 0
current_index = 0
start_time = 0  # Define start_time as a global variable
pomodoro_running = False
timer_mins = 0
# Dummy data for the dropdown menu
projects = []
# Authenticate with Notion API using integration token
notion = Client(auth=integration_token)
# Projects database
database_id = "ef5fcadfa8144d22b2d613a5c86b9cf6"
results = notion.databases.query(database_id).get("results")
# print(results)
# Get the Name column contents
projects = ['']+[page['properties']['Name']['title']
                 [0]['text']['content'] for page in results]
projects.sort()
current_project = projects[0] if projects else ""
current_project = ""


print(token)
print()
