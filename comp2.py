import tkinter as tk
from tkinter import ttk
import requests
import json
import time
import threading
from notion_client import Client
import re


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

#
# dropdown problem seems to lie in readDatabase()... after updating succesfully, it resets back to object mode..
#


def readDatabase(databaseId):
    global results, current_index

    # Query the database and get the results
    results = notion.databases.query(databaseId).get("results")

    # Loop through the list of results - Extraer listas de props.
    for result in results:
        # Get the Name value for the current result, if it exists
        name = ""
        if "Name" in result["properties"] and len(result["properties"]["Name"]["title"]) > 0:
            name = result["properties"]["Name"]["title"][0]["text"]["content"]

        # Get the Note value for the current result, if it exists
        note = ""
        if "Note" in result["properties"] and len(result["properties"]["Note"]["rich_text"]) > 0:
            note = result["properties"]["Note"]["rich_text"][0]["text"]["content"]

        # Get the Project value for the current result, if it exists
        project = ""  # lo imprime muy bn...
        if "Project" in result["properties"] and len(result["properties"]["Project"]["rich_text"]) > 0:
            project = result["properties"]["Project"]["rich_text"][0]["plain_text"]

        # print(f"Result -  Project: {project}")    # prints the project list

    show_result(current_index, project)


def show_result(index, project):
    global name, note, current_index, current_project
    current_index = index
    # print("PROJECT::::::::"+str(project))
    current_project = project

    # Get the page object
    page = results[index]
    # print(results[index]['properties']['Project']
    #   ['rich_text'][0]['text']['content'])

    # Get the name
    name = page['properties']['Name']['title'][0]['text']['content']

    # Get the note
    if 'Note' in page['properties'] and page['properties']['Note']['rich_text']:
        note = page['properties']['Note']['rich_text'][0]['text']['content']
    else:
        note = ""

    # Get the page_id
    page_id = page['id']

    # Update the input_box and props_box widgets with the new information
    input_box.delete('1.0', 'end')
    name_text = f"🪶 {name.strip()}"  # remove newline character
    input_box.insert('1.0', name_text)
    props_box.delete('1.0', 'end')
    note_text = f"📝 {note.strip()}"  # remove newline character
    props_box.insert('1.0', note_text)

    # Set the cursor's default location to the first line with content
    input_box.mark_set("insert", "1.0")

    selected_project = current_project

    # Update the text of the project_button with the name of the project
    if selected_project == "":
        project_text = "No Project"
    else:
        project_text = selected_project
    project_button.config(text=project_text)

    # Set the current project to the one displayed in the current result
    for i in range(menu.index('end')):
        if menu.entrycget(i, 'label') == current_project:
            current_project = menu.entrycget(i, 'label')
            break
    else:
        current_project = ""

    select_project(results[current_index]['properties']
                   ['Project']['rich_text'])


def update_database():
    global name, note, results, current_index, timer_mins, current_project

    page_id = results[current_index]['id']
    name = input_box.get("1.0", 'end').strip()
    note = props_box.get("1.0", 'end').strip()

    print("current project:"+current_project)

    # Remove the "🪶 Log -->" and "📝 Note -->" added text from the name and note variables
    if name.startswith("🪶"):
        name = name[1:]
    if note.startswith("📝"):
        note = note[1:]
    data = {
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": name
                        }
                    }
                ]
            },
            "Note": {
                "rich_text": [
                    {
                        "text": {
                            "content": note
                        }
                    }
                ]
            },
            "Project": {
                "rich_text": [
                    {
                        "text": {
                            "content": current_project
                        }
                    }
                ]
            }
        }
    }
    # print("data:", data)  # debugging line
    # Check if the timer-mins property exists in the data for the current page
    if timer_mins is not None:
        data["properties"]["timer-mins"] = {
            "number": timer_mins
        }

    # Set up the Notion API request headers using your integration token
    headers = {
        "Notion-Version": "2021-08-16",
        "Authorization": token,
        "Content-Type": "application/json"
    }

    # Send a PATCH request to the Notion API to update the page properties
    url = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.patch(url, headers=headers, json=data)

    # If the API request was successful, reload the database and update the results
    if response.status_code == 200:
        readDatabase(databaseId)

        # Change the button icon to a spinner
        a1_button.config(text="updating db...")

        # Set a delay of 1 second before switching the button back to the original icon
        root.after(1000, lambda: a1_button.config(text="💾"))

    # If the API request was unsuccessful, print an error message
    else:
        print(f"Error: {response.status_code} - {response.text}")


def show_next(project):
    global current_index, name, note
    current_index += 1
    if current_index >= len(results):
        current_index = len(results) - 1
    name = input_box.get("1.0", 'end').strip()
    note = props_box.get("1.0", 'end').strip()
    show_result(current_index, project)


def show_prev(project):
    global current_index, name, note
    current_index -= 1
    if current_index < 0:
        current_index = 0
    name = input_box.get("1.0", 'end').strip()
    note = props_box.get("1.0", 'end').strip()
    show_result(current_index, project)


def select_project(project):
    global current_project
    current_project = project
    # Check if the project list is not empty
    if project:
        # Extract the text from the 'content' key using a regular expression
        match = re.search(r"'content': '(.+?)'", str(project))
        if match:
            current_project = match.group(1)

    # Update the text property of the button
    project_button.config(
        text=current_project if current_project else "No Project")


#
# ----------------------------------- Window creation (View) --------------------------------------
#
root = tk.Tk()

overrideredirect_enabled = True

# Remove title bar
root.overrideredirect(True)

# Set the window to always be on top
root.wm_attributes("-topmost", True)

# Set the window size
root.geometry("1069x70+0+1370")

# Set the title of the window
root.title("Active Window 🚀🌙⭐")


root.config(borderwidth=0)
root.configure(background="#1e2127")
root.config(borderwidth=0, bg="#1e2127")

# Calculate the width of the root window
width = root.winfo_screenwidth()

# Create a function to round the edges of buttons
# estilo universal de botones.... *****


# ============ Create frame to hold Right - buttons
frame = tk.Frame(root, bg="#1e2127")
frame.pack(side='right', padx=0)
# Configure column widths
frame.columnconfigure(0, weight=0)
frame.columnconfigure(1, weight=2)
frame.columnconfigure(2, weight=2)


# Create update page button a1
a1_button = tk.Button(frame, text="💾", command=update_database)
a1_button.grid(row=1, column=0, padx=0, pady=0)


# ====== Create frame to hold Left navigation - buttons
frameL = tk.Frame(root, bg="#1e2127")
frameL.pack(side='right', padx=0)

# Create button ↑ Next
a3_button = tk.Button(frameL, text="↑", command=lambda: show_prev(current_project),
                      font=('TkDefaultFont', 14, 'bold'), width=2, height=1, bg="#444B64", relief="flat")
a3_button.grid(row=0, column=0, padx=1, pady=0, sticky="nswe")

# Create button ↓ Prev -  ← ↑ → ↓ ↚ ↛ ↜ ↝ ↞ ↟
a4_button = tk.Button(frameL, text="↓", command=lambda: show_next(current_project),
                      font=('TkDefaultFont', 14, 'bold'), width=2, height=1, bg="#444B64", relief="flat")
a4_button.grid(row=1, column=0, padx=1, pady=0, sticky="nswe")

#
# ------------------------------ input_box, paned_window to hold props_box, options_box
#
# -------------------------- frame input + checkbox
# Create a frame to hold the checkbox and the input box
checkbox_frame = tk.Frame(root, bg="#1e2127")
checkbox_frame.pack(fill='both', expand=True)

# Set the frame's background color to match the input box's background color
checkbox_frame.config(borderwidth=0, bg="#1e2127")

# Create the input box with 90% width
input_box = tk.Text(checkbox_frame, height=1, width=int(
    width*0.9/7), bg="#1e2127", fg="white")

# Add placeholder text
input_box.insert('1.0', f"🪶 Active Log --> {name}\n")

# Set cursor color to white
input_box.config(insertbackground='white')

# Add the input box to the frame
input_box.pack(side='left', fill='both', expand=True)

# Pack the checkbox_frame instead of the input box
checkbox_frame.pack(fill='both', expand=True)
# -----------------------------------------------------------------
# Create paned window to hold note and options columns
paned_window = tk.PanedWindow(
    root, orient=tk.HORIZONTAL, sashwidth=5, sashpad=5, showhandle=True, handlesize=10, bg="#444B64", bd=2)
paned_window.pack(fill='both', expand=True, padx=1, pady=1)

# Create Note column
props_box = tk.Text(paned_window, height=3.7, width=118,
                    bg="#1e2127", fg="white")
props_box.pack(fill='both', expand=True)

# Add placeholder text
props_box.insert('1.0', f"📝 Note --> {note}\n")

# Set cursor color to white
props_box.config(insertbackground='white')

# Create options column
options_box = tk.Text(paned_window, height=1.5, width=10,
                      bg="#1e2127", fg="white")
options_box.pack(fill='both', expand=True)

# Create a frame to hold the new button
button_frame = tk.Frame(options_box, bg="#1e2127")
button_frame.pack(side='left', padx=5)


# Create the new button with updated text
project_text = current_project if current_project != "" else "No Project"
project_button = tk.Button(button_frame, text=project_text,
                           command=lambda: menu.post(project_button.winfo_rootx(), project_button.winfo_rooty()))
project_button.config(width=130, height=4, bg="#444B64",
                      fg="white", activebackground="#343540")
project_button.pack(side='left')


# Create the dropdown menu
menu = tk.Menu(project_button, tearoff=0)

# Add the projects to the dropdown menu
# pareciera que cada projecto lo vuelven un boton con el commando select_project y fija ese.
# ese es el valor con el que hay que actualiozar el current_project q no aaparece el malvado...
for project in projects:
    menu.add_command(
        label=project, command=lambda p=project: select_project(p))


# Add columns to paned window
paned_window.add(props_box)
paned_window.add(options_box)


# Read the database and show the first result
readDatabase(databaseId)
# show_result(current_index, project)

root.mainloop()
