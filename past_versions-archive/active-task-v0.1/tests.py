import tkinter as tk
import requests
import json
import win32gui
import win32con

# Get the window handle
hwnd = win32gui.FindWindow(None, "Log / Active Task")

# Set the window to always be on top
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)

# Remove the always on top flag (when the program exits)
win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)


token = 'secret_Rs800ockGMwCwW6w7SY34v9m2QXtFCkeuqleS77U8Pb'
databaseId = '614f2195f4ee4c9b8db9b232b8d53948'

root = tk.Tk()

# Remove title bar
root.overrideredirect(True)

# Set the window to always be on top
root.wm_attributes("-topmost", True)

# Set the window size
root.geometry("700x80+0+1373")

# Set the title of the window
root.title("Log / Active Task")

root.config(borderwidth=0)
root.configure(background="#29314e")
root.config(borderwidth=0, bg="#29314e")

# Create input box
input_box = tk.Entry(root, width=700, bg="#29314e", fg="white", font=("Arial", 20), bd=0,
                     insertbackground="white", highlightthickness=0, justify="center", selectbackground="#29314e")
input_box.pack(fill="both", expand=True, padx=10, pady=10)

# Add placeholder text
input_box.insert(0, "Active Task --> ")


def readDatabase():
    query_url = f"https://api.notion.com/v1/databases/{databaseId}/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2021-08-16",
        "Content-Type": "application/json",
    }
    query_params = {
        "sorts": [
            {
                "property": "Created time",
                "direction": "descending"
            }
        ],
        "page_size": 1
    }

    response = requests.post(query_url, headers=headers, json=query_params)
    data = response.json()

    if response.status_code == 200:
        if data.get("results"):
            latest_entry = data["results"][0]
            name = latest_entry["properties"]["Name"]["title"][0]["text"]["content"]
            input_box.delete(0, tk.END)
            input_box.insert(0, name)
        else:
            input_box.delete(0, tk.END)
            input_box.insert(0, "No results found")
    else:
        input_box.delete(0, tk.END)
        input_box.insert(
            0, f"Request failed with {response.status_code} - {response.text}")

    with open('./db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)


# Call readDatabase() on program start
readDatabase()

# Set up periodic refresh of the input box


def updateInputBox():
    readDatabase()
    root.after(1000, updateInputBox)


# Start periodic refresh of the input box
root.after(1000, updateInputBox)

root.mainloop()
