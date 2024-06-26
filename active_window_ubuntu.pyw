import os
import tkinter as tk
from tkinter import messagebox
import requests
from notion_client import Client  # Importing the Notion client
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Retrieve environment variables
token = os.getenv('NOTION_API_TOKEN')
logDatabaseId = os.getenv('LOG_DB_ID')

# Headers for HTTP requests
headers = {
    "Authorization": "Bearer " + token,
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Notion API client initialization
notion = Client(auth=token)

# List to store database query results
results = []
current_index = 0

# Define GUI main window
root = tk.Tk()
root.title("Notion Interface")
current_size = "1500x120+1600+2690"
root.geometry(current_size)  # Set initial geometry based on current_size
root.configure(background='#343844')

# Define functions interacting with Notion API
def read_database(database_id):
    global results, current_index
    results = notion.databases.query(database_id).get("results")
    if results:
        show_result(current_index)
    else:
        note_text.delete(1.0, tk.END)
        note_text.insert(tk.END, "No entries found.")

def show_result(index):
    global current_index
    current_index = index
    if results:
        page = results[index]
        note = page['properties']['Note']['rich_text'][0]['text']['content'] if 'Note' in page['properties'] and page['properties']['Note']['rich_text'] else ""
        note_text.delete(1.0, tk.END)
        note_text.insert(tk.END, note)

def update_database(event=None):
    page_id = results[current_index]['id']
    note = note_text.get(1.0, tk.END).strip()
    data = {
        "properties": {
            "Note": {
                "rich_text": [{"text": {"content": note}}]
            }
        }
    }
    response = requests.patch(f"https://api.notion.com/v1/pages/{page_id}", headers=headers, json=data)
    if response.status_code == 200:
        read_database(logDatabaseId)

def next_entry(event=None):
    global current_index
    if current_index < len(results) - 1:
        current_index += 1
        show_result(current_index)

def previous_entry(event=None):
    global current_index
    if current_index > 0:
        current_index -= 1
        show_result(current_index)

def create_page():
    newPageData = {
        "parent": {"database_id": logDatabaseId},
        "properties": {
            "Name": {"title": [{"text": {"content": "New Entry"}}]},
            "Note": {"rich_text": [{"text": {"content": "Type your note here..."}}]}
        }
    }
    response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=newPageData)
    if response.status_code == 200:
        messagebox.showinfo("Success", "New entry created successfully!")
        read_database(logDatabaseId)
    else:
        messagebox.showerror("Error", f"Failed to create new entry: {response.text}")

def toggle_size():
    global current_size
    if current_size == "1400x699+1600+2100":
        root.geometry("1500x120+1600+2690")
        resize_button.config(text="⬜")
        current_size = "1500x120+1600+2690"
    else:
        root.geometry("1400x699+1600+2100")
        resize_button.config(text="◻️")
        current_size = "1400x699+1600+2100"

# Main frame setup
main_frame = tk.Frame(root, bg='#C6C6C6')
main_frame.pack(fill=tk.BOTH, expand=True)

# Text area for note editing
note_text = tk.Text(main_frame, height=4, width=50, bg='#C6C6C6', fg='black', insertbackground='black')
note_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)

# Frame for buttons
button_frame = tk.Frame(main_frame, bg='#C6C6C6')
button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 10), pady=10)

# Column 1: Navigation buttons
nav_button_frame = tk.Frame(button_frame, bg='#C6C6C6')
nav_button_frame.pack(side=tk.LEFT, fill=tk.Y)

prev_button = tk.Button(nav_button_frame, text="↑", command=previous_entry, width=2, bg='#C6C6C6', fg='black')
prev_button.pack(fill=tk.X)

next_button = tk.Button(nav_button_frame, text="↓", command=next_entry, width=2, bg='#C6C6C6', fg='black')
next_button.pack(fill=tk.X)

# Column 2: Action buttons
action_button_frame = tk.Frame(button_frame, bg='#C6C6C6')
action_button_frame.pack(side=tk.LEFT, fill=tk.Y)

create_button = tk.Button(action_button_frame, text="+", command=create_page, width=2, bg='#C6C6C6', fg='black')
create_button.pack(fill=tk.X)

update_button = tk.Button(action_button_frame, text="↻", command=update_database, width=2, bg='#C6C6C6', fg='black')
update_button.pack(fill=tk.X)

# Column 3: Misc buttons (Toggle Size, Empty)
misc_button_frame = tk.Frame(button_frame, bg='#C6C6C6')
misc_button_frame.pack(side=tk.LEFT, fill=tk.Y)

resize_button = tk.Button(misc_button_frame, text="⬛", command=toggle_size, width=2, bg='#C6C6C6', fg='black')
resize_button.pack(fill=tk.X)

empty_button = tk.Button(misc_button_frame, text="", width=2, bg='#C6C6C6')  # Empty button placeholder
empty_button.pack(fill=tk.X)

# Bind Ctrl+Enter to update_database function
root.bind("<Control-Return>", update_database)

# Bind Ctrl+Up Arrow to previous_entry function
root.bind("<Control-Up>", previous_entry)

# Bind Ctrl+Down Arrow to next_entry function
root.bind("<Control-Down>", next_entry)

# Initialize the application by reading the database
read_database(logDatabaseId)

root.mainloop()
