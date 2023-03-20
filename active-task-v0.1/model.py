import tkinter as tk
import requests


class NotionModel:
    def __init__(self, database_id, token):
        self.database_id = database_id
        self.token = token
        self.headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "Notion-Version": "2021-05-13"
        }
        self.results = []

    def read_database(self):
        read_url = f"https://api.notion.com/v1/databases/{self.database_id}/query"

        res = requests.request("POST", read_url, headers=self.headers)
        data = res.json()

        if 'results' not in data:
            print(f"Error: {res.status_code} - {res.text}")
            return

        # Append each name and note pair to the results list
        self.results = []
        for result in data['results']:
            if 'title' in result['properties']['Name'] and result['properties']['Name']['title']:
                name = result['properties']['Name']['title'][0]['plain_text']
            else:
                name = ''
                print(
                    f"Error: 'title' property in 'Name' field is empty for result {result}")
            if 'rich_text' in result['properties']['Note']:
                if result['properties']['Note']['rich_text']:
                    note = result['properties']['Note']['rich_text'][0]['plain_text']
                else:
                    note = ''
            else:
                note = ''
            self.results.append((name, note))


class NotionView:
    def __init__(self, master):
        self.master = master
        self.current_index = 0

        # Create the input box with 90% width
        self.input_box = tk.Text(
            self.master, height=1.5, width=100, bg="#29314e", fg="white")
        self.input_box.pack(fill='both', expand=True)

        # Set cursor color to white
        self.input_box.config(insertbackground='white')

        # Create paned window to hold note and options columns
        self.paned_window = tk.PanedWindow(
            self.master, orient=tk.HORIZONTAL, sashwidth=5, sashpad=5, showhandle=True, handlesize=10)
        self.paned_window.pack(fill='both', expand=True, padx=5, pady=5)

        # Create Note column
        self.props_box = tk.Text(
            self.paned_window, height=1.5, width=118, bg="#29314e", fg="white")
        self.props_box.pack(fill='both', expand=True)

        # Set cursor color to white
        self.props_box.config(insertbackground='white')

        # Create options column
        self.options_box = tk.Text(self.paned_window, height=1.5, width=10,
                                   bg="#29314e", fg="white")
        self.options_box.pack(fill='both', expand=True)

        # Add placeholder text
        self.options_box.insert(
            '1.0', "Options: send to Notes/Tasks, add/edit Tags. ")

        # Add columns to paned window
        self.paned_window.add(self.props_box)
        self.paned_window.add(self.options_box)

        # Create frame to hold buttons
        self.frame = tk.Frame(self.master, bg="#29314e")
        self.frame.pack(side='right', padx=1)

        # Create size button
        self.current_size = "1050x20"
        self.size_button = tk.Button(
            self.frame, text="Toggle Size", command=self.toggle_size)
        self.round_button(self.size_button)
        self.size_button.pack(side='right', padx=5, pady=0, anchor='ne')

        # Create move/lock button
        self.move_button = tk.Button(
            self.frame, text="move/lock", command=self.on_button_click)
        self.round_button(self.move_button)
        self.move_button.pack(side='right', padx=5, pady=0, anchor='ne')

        # Create button a3
        self.a3_button = tk.Button(
            self.frame, text="↑ Next", command=self.show_prev, font=('TkDefaultFont', 12, 'bold'))
        self.round_button(self.a3_button)
        self.a3_button.pack(side='top', padx=5, pady=0, anchor='ne')

        # Create button a4 -  ← ↑ → ↓ ↚ ↛ ↜ ↝ ↞ ↟
        self.a4_button = tk.Button(
            self.frame, text="↓ Prev", command=self.show_next, font=('TkDefaultFont', 12, 'bold'))
        self.round_button(self.a4_button)
        self.a4_button.pack(side='top', padx=5, pady=0, anchor='ne')

    def show_result(self):
        name, note = self.notion.results[self.current_index]
        self.input_box.delete('1.0', tk.END)
        self.input_box.insert('1.0', f"🪶 Active Log --> {name}\n")
        self.props_box.delete('1.0', tk.END)
        self.props_box.insert('1.0', f"📝 Note: --> {note}\n")

    def show_next(self):
        self.current_index += 1
        if self.current_index >= len(self.notion.results):
            self.current_index = len(self.notion.results) - 1
        self.show_result()

    def show_prev(self):
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = 0
        self.show_result()

    def round_button(self, widget):
        widget.config(relief="flat", borderwidth=0, highlightthickness=0)
        widget.config(bg="#343540", fg="#FFFFFF", activebackground="#29314e")
        widget.config(highlightbackground="#29314e", highlightcolor="#29314e")
        widget.config(bd=0, padx=10, pady=5, font=(
            "Arial", 9), width=6, height=2)

    def toggle_size(self):
        if self.current_size == "1050x20":
            self.master.geometry("500x500+0+973")
            self.current_size = "500x500"
        else:
            self.master.geometry("1050x70+0+1373")
            self.current_size = "1050x20"

    def on_button_click(self):
        self.toggle_overrideredirect()

    def toggle_overrideredirect(self):
        self.overrideredirect_enabled = not self.overr

    def toggle_overrideredirect(self):
        self.overrideredirect_enabled = not self.overrideredirect_enabled
        self.master.overrideredirect(self.overrideredirect_enabled)


class NotionController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Active Window")
        self.root.config(borderwidth=0, bg="#29314e")
        # Set the window to always be on top
        self.root.wm_attributes("-topmost", True)

        # Remove title bar
        self.root.overrideredirect(True)

        self.notion = NotionModel(database_id='614f2195f4ee4c9b8db9b232b8d53948',
                                  token='secret_Rs800ockGMwCwW6w7SY34v9m2QXtFCkeuqleS77U8Pb')
        self.view = NotionView(self.root)
        self.view.notion = self.notion

        self.view.show_result()

        self.root.mainloop()


if __name__ == '__main__':
    controller = NotionController()
