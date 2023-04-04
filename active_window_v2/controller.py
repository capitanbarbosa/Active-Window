
#
# ------------------ (Controller) -------------------------
#
import tkinter as tk
from tkinter import ttk
import requests
import json
import time
import threading
import re


def readDatabase(databaseId):
    global results

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

        # Get the Active? value for the current result, if it exists
        active = False
        if "Active?" in result["properties"] and result["properties"]["Active?"]["checkbox"]:
            active = result["properties"]["Active?"]["checkbox"]

        # Get the Project value for the current result, if it exists
        project = ""  # lo imprime muy bn...
        if "Project" in result["properties"] and len(result["properties"]["Project"]["rich_text"]) > 0:
            project = result["properties"]["Project"]["rich_text"][0]["plain_text"]

    # Set the state of the tkinter Checkbox widget to match the "Active?" column value of the current page
    checkbox.var.set(results[current_index]
                     ['properties']['Active?']['checkbox'])

    show_result(current_index, project)


def show_result(index, project):
    global name, note, current_index, current_project
    current_index = index
    current_project = project

    # Get the page object
    page = results[index]

    # Get the name
    # name = page['properties']['Name']['title'][0]['text']['content']
    if 'Name' in page['properties'] and page['properties']['Name']['title']:
        name = page['properties']['Name']['title'][0]['text']['content']
    else:
        name = ""

    # Get the note
    if 'Note' in page['properties'] and page['properties']['Note']['rich_text']:
        note = page['properties']['Note']['rich_text'][0]['text']['content']
    else:
        note = ""

    # Get the page_id
    page_id = page['id']

    # Get the active status
    if 'Active?' in page['properties']:
        active = page['properties']['Active?']['checkbox']
    else:
        active = False

    # Update the input_box and props_box widgets with the new information
    input_box.delete('1.0', 'end')
    name_text = f"🪶 {name.strip()}"  # remove newline character
    input_box.insert('1.0', name_text)
    props_box.delete('1.0', 'end')
    note_text = f"📝 {note.strip()}"  # remove newline character
    props_box.insert('1.0', note_text)

    # Set the cursor's default location to the first line with content
    input_box.mark_set("insert", "1.0")
    checkbox.var.set(active)

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

    # Add this check at the beginning of the update_database function
    if isinstance(current_project, list) and not current_project:
        current_project = ""

    page_id = results[current_index]['id']
    name = input_box.get("1.0", 'end').strip()
    note = props_box.get("1.0", 'end').strip()

    print("current project:"+str(current_project))

    # Remove the "🪶 Log -->" and "📝 Note -->" added text from the name and note variables
    if name.startswith("🪶"):
        name = name[1:]
    if note.startswith("📝"):
        note = note[1:]

    # Create the data dictionary, excluding the "Project" property if current_project is empty
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
            },
        }
    }

    # Add the "Project" property if current_project is not empty
    # if current_project is None:
    #     data["properties"]["Project"] = {
    #         "rich_text": [
    #             {
    #                 "text": {
    #                     "content": current_project
    #                 }
    #             }
    #         ]
    #     }

    # chatGPT always fucks us here, switching the is None -> is not . we always fix this here...
    #   the timer updating to 0 always...
    # Check if the timer-mins property exists in the data for the current page
    if timer_mins is None:
        data["properties"]["timer-mins"] = {
            "number": timer_mins
        }

    # Check the state of the checkbox and modify the data dictionary accordingly
    if checkbox.var.get() == 1:
        data["properties"]["Active?"] = {
            "checkbox": True
        }
    else:
        data["properties"]["Active?"] = {
            "checkbox": False
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


def createPage(databaseId, headers):

    createUrl = 'https://api.notion.com/v1/pages'

    newPageData = {
        "parent": {"database_id": databaseId},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": ""
                        }
                    }
                ]
            },
            "Note": {
                "rich_text": [
                    {
                        "text": {
                            "content": ""
                        }
                    }
                ]
            }
        }
    }
    if timer_mins is None:
        newPageData["properties"]["timer-mins"] = {
            "number": timer_mins
        }

    # # Add the "Project" property if current_project is not empty
    # if current_project is None:
    #     newPageData["properties"]["Project"] = {
    #         "rich_text": [
    #             {
    #                 "text": {
    #                     "content": current_project
    #                 }
    #             }
    #         ]
    #     }

    # print(databaseId, headers, name, note)
    data = json.dumps(newPageData)

    res = requests.request("POST", createUrl, headers=headers, data=data)

    print(res.status_code)
    # print(res.text)
    update_database()


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


def move_lock():
    if "🔒" in move_button["text"]:
        move_button.config(text="🔓")
    else:
        move_button.config(text="🔒")
    toggle_overrideredirect()


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


def toggle_overrideredirect():
    global overrideredirect_enabled
    overrideredirect_enabled = not overrideredirect_enabled
    root.overrideredirect(overrideredirect_enabled)


def toggle_size():
    global current_size
    if current_size == "1069x21":
        root.geometry("900x500+0+973")
        size_button.config(text="⬜")
        current_size = "900x500"
    else:
        root.geometry("1069x72+0+1370")
        size_button.config(text=" ◻️")
        current_size = "1069x21"


def update_timer():
    global pomodoro_running

    if pomodoro_running:
        start_time = time.time()  # initialize start_time before the loop
        while pomodoro_running:
            time.sleep(1)
            elapsed_time = int(time.time() - start_time)
            minutes = str(elapsed_time // 60).zfill(2)
            seconds = str(elapsed_time % 60).zfill(2)
            pomodoro_button.config(text=f"{minutes}:{seconds}")
            root.update()  # Update the button text immediately

        # Reset the button text and the pomodoro_running variable
        pomodoro_button.config(text="⏰")


def toggle_timer():
    global pomodoro_running, pomodoro_button, start_time, timer_mins

    # Query the current page ID that is being viewed in Notion
    print(results[current_index])
    page_id = results[current_index]['id']
    # Send a GET request to Notion API to retrieve the "timer-mins" property of the current page
    res = requests.get(
        f"https://api.notion.com/v1/pages/{page_id}", headers=headers)
    data = res.json()

    if 'properties' in data and 'timer-mins' in data['properties']:
        timer_mins = data['properties']['timer-mins']['number']
        print(timer_mins)
    else:
        timer_mins = None  # set the value of timer_mins to None if it is null or blank

    if pomodoro_running:
        # Stop the timer and change the button text back to the icon
        pomodoro_running = False
        pomodoro_button.config(text="⏰")

        # Calculate total elapsed time
        if start_time is not None:
            if timer_mins is not None:
                elapsed_time = int(time.time() - start_time) + \
                    (timer_mins * 60)
            else:
                elapsed_time = int(time.time() - start_time)

            # Calculate minutes and seconds from elapsed time
            minutes = elapsed_time // 60

            # Update the "timer-mins" property of the current page with the elapsed time in minutes
            data = {
                "properties": {
                    "timer-mins": {
                        "number": minutes
                    }
                }
            }
            response = requests.patch(
                f"https://api.notion.com/v1/pages/{page_id}", headers=headers, json=data)
            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")

            # Create label to display total time and add to root window
            total_time = f"Total Time: {minutes} minutes"
            total_time_label = tk.Label(root, text=total_time, font=(
                'Arial', 12), bg='#1e2127', fg='white')
            total_time_label.pack(side='top')

            # Remove total time label after 10 seconds
            root.after(10000, total_time_label.destroy)

    else:
        # Start the timer and change the button text to show the elapsed time
        pomodoro_running = True
        start_time = time.time()
        if timer_mins is not None:
            pomodoro_button.config(text=f"{timer_mins:02d}:00")
        t = threading.Thread(target=update_timer)
        t.start()
