import tkinter as tk
from tkinter import ttk
import requests
import json
import time
import threading
from notion_client import Client
import pprint
import re

#
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

#
# ------------------ (Controller) -------------------------
#


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
            }
        }
    }

    # Add the "Project" property if current_project is not empty
    if current_project:
        data["properties"]["Project"] = {
            "rich_text": [
                {
                    "text": {
                        "content": current_project
                    }
                }
            ]
        }

    # Check if the timer-mins property exists in the data for the current page
    if timer_mins is not None:
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
root.geometry("1081x70+0+1370")

# Set the title of the window
root.title("Active Window 🚀🌙⭐")


root.config(borderwidth=0)
root.configure(background="#1e2127")
root.config(borderwidth=0, bg="#1e2127")

# Calculate the width of the root window
width = root.winfo_screenwidth()

# Create a function to round the edges of buttons
# estilo universal de botones.... *****


def round_button(widget):
    widget.config(relief="flat", borderwidth=1, highlightthickness=1)
    widget.config(bg="#1e2127", fg="#FFFFFF", activebackground="#1e2127")
    widget.config(highlightbackground="white", highlightcolor="white")
    widget.config(bd=2, padx=5, pady=0, font=("Arial", 9), width=6, height=2)
    widget.config(padx=0)
    widget.config(highlightthickness=1, highlightbackground='white')


# keeb shortcuts -> ctrl + k, ctrl up and down


def on_key_press(event):
    if event.state == 4 and event.keysym == "Return":
        a1_button.invoke()
        print("ctrl enter pressed")


def handle_ctrl_up(event):
    # Handle Ctrl + Up keypress here
    a3_button.invoke()


def handle_ctrl_down(event):
    # Handle Ctrl + Down keypress here
    pass
    a4_button.invoke()


# ============ Create frame to hold Right - buttons
frame = tk.Frame(root, bg="#1e2127")
frame.pack(side='right', padx=0)
# Configure column widths
frame.columnconfigure(0, weight=0)
frame.columnconfigure(1, weight=2)
frame.columnconfigure(2, weight=2)

# Create add-plus button
plus_button = tk.Button(
    frame, text="+", command=lambda: createPage(databaseId, headers))
round_button(plus_button)
plus_button.grid(row=0, column=0, padx=0, pady=0)

# Create update page button a1
a1_button = tk.Button(frame, text="💾", command=update_database)
round_button(a1_button)
a1_button.grid(row=1, column=0, padx=0, pady=0)

# Create toggle size button
current_size = "1069x21"
size_button = tk.Button(frame, text="⬛", command=toggle_size)
round_button(size_button)
size_button.grid(row=0, column=2, padx=0, pady=0)

# Create move/lock button
move_button = tk.Button(frame, text="🔒", command=move_lock)
round_button(move_button)
move_button.grid(row=1, column=2, padx=0, pady=0)

# Create pomodoro button
pomodoro_button = tk.Button(frame, text="⏰", command=toggle_timer)
round_button(pomodoro_button)
pomodoro_button.grid(row=0, column=1, padx=0, pady=0)

root.bind("<Key>", on_key_press)
root.bind('<Control-Up>', handle_ctrl_up)
root.bind('<Control-Down>', handle_ctrl_down)

# Create magic button a2
a2_button = tk.Button(frame, text="🪄")
round_button(a2_button)
a2_button.grid(row=1, column=1, padx=0, pady=0)


# ====== Create frame to hold Left navigation - buttons
frameL = tk.Frame(root, bg="#1e2127")
frameL.pack(side='right', padx=0)
arrow_buttons_bg = "#3f4652"

# Create button ↑ Next
a3_button = tk.Button(frameL, text="↑", command=lambda: show_prev(current_project),
                      font=('TkDefaultFont', 14, 'bold'), width=2, height=1, bg=arrow_buttons_bg, relief="flat")
a3_button.grid(row=0, column=0, padx=1, pady=0, sticky="nswe")

# Create button ↓ Prev -  ← ↑ → ↓ ↚ ↛ ↜ ↝ ↞ ↟
a4_button = tk.Button(frameL, text="↓", command=lambda: show_next(current_project),
                      font=('TkDefaultFont', 14, 'bold'), width=2, height=1, bg=arrow_buttons_bg, relief="flat")
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

# Create the checkbox
checkbox = tk.Checkbutton(
    checkbox_frame, bg="#1e2127", highlightthickness=0)

# Add the checkbox to the frame
checkbox.pack(side='right')

# Set the checkbox's background color to match the input box's background color
checkbox.config(bg="#1e2127")


# Create a variable to hold the state of the checkbox
checkbox.var = tk.IntVar()

# Set the initial state of the checkbox to unchecked
checkbox.var.set(0)

# Bind the checkbox to the callback function
checkbox.config(variable=checkbox.var, command=update_database)


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
    root, orient=tk.HORIZONTAL, sashwidth=5, sashpad=5, showhandle=True, handlesize=10, bg=arrow_buttons_bg, bd=2)
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
project_button.config(width=130, height=4, bg=arrow_buttons_bg,
                      fg="white", activebackground="#1e2127")
project_button.pack(side='left')


# Create the dropdown menu
menu = tk.Menu(project_button, tearoff=0)

# Add the projects to the dropdown menu
# pareciera que cada projecto lo vuelven un boton con el commando select_project y fija ese.
# ese es el valor con el que hay que actualiozar el current_project q no aaparece el malvado...
for project in projects:
    menu.add_command(
        label=project, command=lambda p=project: select_project(p))


# Create the new button2
new_button2 = tk.Button(button_frame, text="add/edit Tags",
                        command=lambda: print("New Button Clicked!"))
new_button2.config(width=10, height=1, bg=arrow_buttons_bg,
                   fg="white", activebackground="#1e2127")
new_button2.pack(side='left')

# Create the new button3
new_button3 = tk.Button(button_frame, text="link to note/task",
                        command=lambda: print("New Button Clicked!"))
new_button3.config(width=10, height=1, bg=arrow_buttons_bg,
                   fg="white", activebackground="#1e2127")
new_button3.pack(side='left')

# Create the new button4
new_button4 = tk.Button(button_frame, text="wiz commands",
                        command=lambda: print("New Button Clicked!"))
new_button4.config(width=10, height=1, bg=arrow_buttons_bg,
                   fg="white", activebackground="#1e2127")
new_button4.pack(side='left')


# Add columns to paned window
paned_window.add(props_box)
paned_window.add(options_box)


# Read the database and show the first result
readDatabase(databaseId)
# show_result(current_index, project)

root.mainloop()
