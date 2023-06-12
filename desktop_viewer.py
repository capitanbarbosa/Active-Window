import tkinter as tk
from tkinter import ttk
import requests
import json
import time
import threading
from notion_client import Client
import pprint
import re
# import tkinter.simpledialog as simpledialog
from tkinter import simpledialog, messagebox
import keyboard
import ctypes


import pyautogui



class ShortcutButtonRow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.buttons = []
        self.shift_pressed = False  # Variable to track the state of the shift key
        self.create_widgets()
        self.create_shift_listener()  # Create the global shift key listener

    def create_shift_listener(self):
        # Create a global listener for the shift key
        keyboard.on_press_key("shift", self.on_shift_key_press)
        keyboard.on_release_key("shift", self.on_shift_key_release)

    def on_shift_key_press(self, event):
        # Change the background color of the framey frame and buttons when Shift key is pressed
        self.shift_pressed = True  # Set the shift_pressed flag to True
        for button in self.buttons:
            button.config(bg="#0077CC")  # Set the background color of buttons to red

    def on_shift_key_release(self, event):
        # Change the background color of the framey frame and buttons back to the default color when Shift key is released
        self.shift_pressed = False  # Set the shift_pressed flag to False
        for button in self.buttons:
            button.config(bg="#3f4652")  # Set the background color of buttons to the default color


    def create_widgets(self):
        # Create a frame to hold the buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.LEFT)

        # # Create the "+" button to add more buttons
        # self.add_button = tk.Button(self.button_frame, text="  +  ", command=self.create_button, relief=tk.FLAT, bg="#3f4652")
        # self.add_button.pack(side=tk.LEFT)

        # Create the initial buttons
        self.create_default_buttons()

    def create_default_buttons(self):
        # Create the "Log" button
        self.create_button(name="Log", bg="#3f4699")  # Set the background color of the button to black
        self.create_button(name="dev", bg="#3f4652")  # Set the background color of the button to black
        self.create_button(name="1", bg="#3f4652")  # Set the background color of the button to black
        self.create_button(name="2", bg="#3f4652")  # Set the background color of the button to black
        self.create_button(name="3", bg="#3f4652")  # Set the background color of the button to black
        self.create_button(name="4", bg="#3f4652")  # Set the background color of the button to black
        self.create_button(name="5", bg="#3f4652")  # Set the background color of the button to black


        # # Create buttons with numbers 2 to 6
        # for index in range(2, 7):
        #     self.create_button(name=str(index), bg="#3f4652")  # Set the background color of the button to black

    def create_button(self, name="", padx=5, bg="#3f4652"):
        # Determine the index of the button in the list
        index = len(self.buttons) + 1

        # Set the text based on the index and name
        if index in [1, 2, 3, 4, 5, 6, 7] and name:
            text = name
        else:
            text = str(index)

        # Create a new button and add it to the button frame
        button = tk.Button(
            self.button_frame,
            text=(" " + text + " ").center(padx),
            relief=tk.FLAT,
            bg=bg,
            fg="white"
        )
        button.pack(side=tk.LEFT)

        # Bind button press event to execute_shortcut method
        button.bind("<ButtonPress-1>", lambda event, idx=index: self.execute_shortcut(idx, event.state))

        # Bind right-click event to edit_button_text method
        button.bind("<Button-3>", lambda event, btn=button: self.edit_button_text(btn))

        # Add the button to the list
        self.buttons.append(button)




    def edit_button_text(self, button):
        # Get the current text of the button
        current_text = button.cget("text").strip()

        # Prompt the user to enter the new text for the button
        new_text = simpledialog.askstring("Edit Button", "Enter the new text for the button:", initialvalue=current_text)

        # Update the button's text if the user provided new text
        if new_text:
            button.config(text=(" " + new_text + " ").center(5))


    def execute_shortcut(self, index, state):
        # Convert the index to a string
        index_str = str(index)

        if state & 0x1:  # If the shift key is pressed
            pyautogui.keyDown('alt')  # Simulate pressing the Alt key
            pyautogui.press('tab')  # Simulate pressing the Tab key
            pyautogui.keyUp('alt')  # Simulate releasing the Alt key
        else:
            # Simulate pressing the Win, Alt
            pyautogui.keyDown('win')
            pyautogui.keyDown('alt')
            pyautogui.keyDown('shift')

            # Simulate pressing the index key (button number)
            pyautogui.press(index_str)

        # Simulate releasing the Win, Alt, Shift, and index keys
        pyautogui.keyUp('win')
        pyautogui.keyUp('alt')
        pyautogui.keyUp('shift')


def on_shift_key_press(event):
    # Change the background color of the framey frame and buttons when Shift key is pressed
    # framey.config(bg="#")  # Set the background color of framey frame to red
    for button in row.buttons:
        button.config(bg="#31887A")  # Set the background color of buttons to red


def on_shift_key_release(event):
    # Change the background color of the framey frame and buttons back to the default color when Shift key is released
    # framey.config(bg="#1e2127")  # Set the background color of framey frame to the default color
    for button in row.buttons:
        button.config(bg="#3f4652")  # Set the background color of buttons to the default color





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
root.geometry("1300x70+0+1370")
# root.minsize(600,600)

# # set initial position
# root.geometry("+0+1370")

# Set the title of the window
root.title("Active Window 🚀🌙⭐")


root.config(borderwidth=0)
root.configure(background="#1e2127")
root.config(borderwidth=0, bg="#1e2127")

# Calculate the width of the root window
width = root.winfo_screenwidth()


# Create the framey frame
framey = tk.Frame(root, bg="#1e2127")
framey.pack(side='right', padx=0, fill=tk.Y, expand=True)

# Create the ShortcutButtonRow component
row = ShortcutButtonRow(framey)
row.pack(side=tk.RIGHT, anchor=tk.N)

# Bind Shift key press and release events to change the background color of framey frame
# root.bind_all("<Shift-Key>", on_shift_key_press)
# root.bind_all("<KeyRelease-Shift_L>", on_shift_key_release)

root.bind_all("<Control-Key>", on_shift_key_press)
root.bind_all("<KeyRelease-Control_L>", on_shift_key_release)



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
        print("ctrl enter pressed")



# ============ Create frame to hold Right - buttons
frame = tk.Frame(root, bg="#1e2127")
frame.pack(side='right', padx=0)
# Configure column widths
frame.columnconfigure(0, weight=0)
frame.columnconfigure(1, weight=2)
frame.columnconfigure(2, weight=2)


root.bind("<Key>", on_key_press)



# ====== Create frame to hold Left navigation - buttons
frameL = tk.Frame(root, bg="#1e2127")
frameL.pack(side='right', padx=0)
arrow_buttons_bg = "#3f4652"


#
# ------------------------------ input_box, paned_window to hold props_box, options_box
#

# Create paned window to hold note and options columns
paned_window = tk.PanedWindow(
    root, orient=tk.HORIZONTAL, sashwidth=5, sashpad=5, showhandle=True, handlesize=10, bg=arrow_buttons_bg, bd=2)
paned_window.pack(fill='both', expand=True, padx=1, pady=1)

# Create Note column
props_box = tk.Text(paned_window, height=3.7, width=118,
                    bg="#1e2127", fg="white")
props_box.pack(fill='both', expand=True)

# Add placeholder text
# props_box.insert('1.0', f"📝 Note --> {note}\n")

# Set cursor color to white
props_box.config(insertbackground='white')

# Create options column
options_box = tk.Text(paned_window, height=1.5, width=10,
                      bg="#1e2127", fg="white")
options_box.pack(fill='both', expand=True)

# Create a frame to hold the new button
button_frame = tk.Frame(options_box, bg="#1e2127")
button_frame.pack(side='left', padx=5)

# Add columns to paned window
paned_window.add(props_box)
paned_window.add(options_box)


root.mainloop()
