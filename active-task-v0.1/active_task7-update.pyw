import tkinter as tk
import requests
import json
import time
import threading


#
# ----------------------- DATA STRUCTURE - MODEL ---------------------
#

token = 'secret_Rs800ockGMwCwW6w7SY34v9m2QXtFCkeuqleS77U8Pb'
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


#
# ------------------ Button commands (Controller) -------------------------
#


def show_result(index):
    global name, note
    name, note, page_id = results[index]

    # Update the input_box and props_box widgets with the new information
    input_box.delete('1.0', 'end')
    name_text = f"🪶 {name.strip()}"  # remove newline character
    input_box.insert('1.0', name_text)
    props_box.delete('1.0', 'end')
    note_text = f"📝 {note.strip()}"  # remove newline character
    props_box.insert('1.0', note_text)

    # Set the cursor's default location to the first line with content
    input_box.mark_set("insert", "1.0")


def readDatabase(databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()

    if 'results' not in data:
        print(f"Error: {res.status_code} - {res.text}")
        return

    # Append each name, note, and page ID tuple to the results list
    global results
    results = []
    for result in data['results']:
        if 'title' in result['properties']['Name'] and result['properties']['Name']['title']:
            name = result['properties']['Name']['title'][0]['plain_text']
        else:
            name = ''
            # print(
            #     f"Error: 'title' property in 'Name' field is empty for result {result}")
        if 'rich_text' in result['properties']['Note']:
            if result['properties']['Note']['rich_text']:
                note = result['properties']['Note']['rich_text'][0]['plain_text']
            else:
                note = ''
        else:
            note = ''
        page_id = result['id']
        results.append((name, note, page_id))

    # print(f"Results: {results}")
    show_result(current_index)


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


def update_database():
    global name, note, results, current_index, timer_mins
    page_id = results[current_index][2]
    name = input_box.get("1.0", 'end').strip()
    note = props_box.get("1.0", 'end').strip()
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
            }
        }
    }

    # Check if the timer-mins property exists in the data for the current page
    if timer_mins is None:
        data["properties"]["timer-mins"] = {
            "number": timer_mins
        }

    # Change the button icon to a spinner
    a1_button.config(text="🔄")

    response = requests.patch(
        f"https://api.notion.com/v1/pages/{page_id}", headers=headers, json=data)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")

    # Set a delay of 1 second before switching the button back to the original icon
    root.after(1000, lambda: a1_button.config(text="💾"))

    readDatabase(databaseId, headers)


def move_lock():
    if "🔒" in move_button["text"]:
        move_button.config(text="🔓")
    else:
        move_button.config(text="🔒")
    toggle_overrideredirect()


def show_next():
    global current_index, name, note
    current_index += 1
    if current_index >= len(results):
        current_index = len(results) - 1
    name = input_box.get("1.0", 'end').strip()
    note = props_box.get("1.0", 'end').strip()
    show_result(current_index)


def show_prev():
    global current_index, name, note
    current_index -= 1
    if current_index < 0:
        current_index = 0
    name = input_box.get("1.0", 'end').strip()
    note = props_box.get("1.0", 'end').strip()
    show_result(current_index)


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
    page_id = results[current_index][2]

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
                'Arial', 12), bg='#29314e', fg='white')
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
root.geometry("1069x70+0+1370")

# Set the title of the window
root.title("Active Window 🚀🌙⭐")


root.config(borderwidth=0)
root.configure(background="#29314e")
root.config(borderwidth=0, bg="#29314e")

# Calculate the width of the root window
width = root.winfo_screenwidth()

# Create a function to round the edges of buttons

#
# ------------------ Buttons frame and grid and design
#

# estilo universal de botones.... *****


def round_button(widget):
    widget.config(relief="flat", borderwidth=1, highlightthickness=1)
    widget.config(bg="#343540", fg="#FFFFFF", activebackground="#29314e")
    widget.config(highlightbackground="white", highlightcolor="white")
    widget.config(bd=2, padx=5, pady=0, font=("Arial", 9), width=6, height=2)
    widget.config(padx=0)
    widget.config(highlightthickness=1, highlightbackground='white')


# ============ Create frame to hold Right - buttons
frame = tk.Frame(root, bg="#29314e")
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


root.bind("<Key>", on_key_press)
root.bind('<Control-Up>', handle_ctrl_up)
root.bind('<Control-Down>', handle_ctrl_down)

# Create magic button a2
a2_button = tk.Button(frame, text="🪄")
round_button(a2_button)
a2_button.grid(row=1, column=1, padx=0, pady=0)


# ====== Create frame to hold Left navigation - buttons
frameL = tk.Frame(root, bg="#29314e")
frameL.pack(side='right', padx=0)

# Create button ↑ Next
a3_button = tk.Button(frameL, text="↑", command=show_prev,
                      font=('TkDefaultFont', 14, 'bold'), width=2, height=1, bg="#444B64", relief="flat")
a3_button.grid(row=0, column=0, padx=1, pady=0, sticky="nswe")

# Create button ↓ Prev -  ← ↑ → ↓ ↚ ↛ ↜ ↝ ↞ ↟
a4_button = tk.Button(frameL, text="↓", command=show_next,
                      font=('TkDefaultFont', 14, 'bold'), width=2, height=1, bg="#444B64", relief="flat")
a4_button.grid(row=1, column=0, padx=1, pady=0, sticky="nswe")

#
# ------------------------------ input_box, paned_window to hold props_box, options_box
#

# Create the input box with 90% width
input_box = tk.Text(root, height=1, width=int(
    width*0.9/7), bg="#29314e", fg="white")
input_box.pack(fill='both', expand=True)

# Add placeholder text
input_box.insert('1.0', f"🪶 Active Log --> {name}\n")


# Set cursor color to white
input_box.config(insertbackground='white')

# Create paned window to hold note and options columns
paned_window = tk.PanedWindow(
    root, orient=tk.HORIZONTAL, sashwidth=5, sashpad=5, showhandle=True, handlesize=10, bg="#444B64", bd=2)
paned_window.pack(fill='both', expand=True, padx=1, pady=1)

# Create Note column
props_box = tk.Text(paned_window, height=1.5, width=118,
                    bg="#29314e", fg="white")
props_box.pack(fill='both', expand=True)

# Add placeholder text
props_box.insert('1.0', f"📝 Note --> {note}\n")

# Set cursor color to white
props_box.config(insertbackground='white')

# Create options column
options_box = tk.Text(paned_window, height=1.5, width=10,
                      bg="#29314e", fg="white")
options_box.pack(fill='both', expand=True)

# Create a frame to hold the new button
button_frame = tk.Frame(options_box, bg="#29314e")
button_frame.pack(side='left', padx=5)

# Create the new button
new_button = tk.Button(button_frame, text="link to note/task",
                       command=lambda: print("New Button Clicked!"))
new_button.config(width=10, height=1, bg="#444B64",
                  fg="white", activebackground="#343540")
new_button.pack(side='left')

# Create the new button2
new_button2 = tk.Button(button_frame, text="add/edit Tags",
                        command=lambda: print("New Button Clicked!"))
new_button2.config(width=10, height=1, bg="#444B64",
                   fg="white", activebackground="#343540")
new_button2.pack(side='left')

# Create the new button3
new_button3 = tk.Button(button_frame, text="add/edit Tags",
                        command=lambda: print("New Button Clicked!"))
new_button3.config(width=10, height=1, bg="#444B64",
                   fg="white", activebackground="#343540")
new_button3.pack(side='left')


# Add columns to paned window
paned_window.add(props_box)
paned_window.add(options_box)


# Read the database and show the first result
readDatabase(databaseId, headers)
show_result(current_index)

root.mainloop()
