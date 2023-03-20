class NotionController:
    def __init__(self, model):
        self.model = model


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
    if timer_mins is not None:
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
