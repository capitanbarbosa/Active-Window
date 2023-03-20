import tkinter as tk


class View:

    def __init__(self, controller):
        self.controller = controller

        self.current_index = 0

        self.root = tk.Tk()
        self.root.title("Active Window")

        # Set the window to always be on top
        self.root.wm_attributes("-topmost", True)

        self.create_widgets()

        self.root.mainloop()

    def create_widgets(self):
        self.create_input_box()
        self.create_props_box()
        self.create_options_box()
        self.create_buttons()

    def create_input_box(self):
        self.input_box = tk.Text(
            self.root, height=1.5, width=60, bg="#29314e", fg="white")
        self.input_box.pack(fill='both', expand=True)

        # Add placeholder text
        self.input_box.insert('1.0', "🪶 Active Log -->")

        # Set cursor color to white
        self.input_box.config(insertbackground='white')

    def create_props_box(self):
        self.props_box = tk.Text(
            self.root, height=1.5, width=60, bg="#29314e", fg="white")
        self.props_box.pack(fill='both', expand=True)

        # Add placeholder text
        self.props_box.insert('1.0', "📝 Note: -->")

        # Set cursor color to white
        self.props_box.config(insertbackground='white')

    def create_options_box(self):
        self.options_box = tk.Text(
            self.root, height=1.5, width=10, bg="#29314e", fg="white")
        self.options_box.pack(fill='both', expand=True)

        # Add placeholder text
        self.options_box.insert(
            '1.0', "Options: send to Notes/Tasks, add/edit Tags. ")

    def create_buttons(self):
        self.prev_button = tk.Button(
            self.root, text="Prev", command=self.show_prev)
        self.prev_button.pack(side="left")

        self.next_button = tk.Button(
            self.root, text="Next", command=self.show_next)
        self.next_button.pack(side="left")

        self.lock_button = tk.Button(
            self.root, text="Lock", command=self.on_lock_button_click)
        self.lock_button.pack(side="right")

        self.size_button = tk.Button(
            self.root, text="Size", command=self.on_size_button_click)
        self.size_button.pack(side="right")

    def show_result(self, name, note):
        self.input_box.delete('1.0', 'end')
        self.input_box.insert('1.0', f"🪶 Active Log --> {name}\n")

        self.props_box.delete('1.0', 'end')
        self.props_box.insert('1.0', f"📝 Note: --> {note}\n")

    def on_lock_button_click(self):
        self.controller.on_lock_button_click()

    def on_size_button_click(self):
        self.controller.on_size_button_click()

    def show_next(self):
        self.current_index += 1
        self.controller.show_result(self.current_index)

    def show_prev(self):
        self.current_index -= 1
        self.controller.show_result(self.current_index)
