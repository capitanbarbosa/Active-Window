import tkinter as tk
from tkinter import ttk
import time
# import tkinter.simpledialog as simpledialog
from tkinter import simpledialog, messagebox
import keyboard
import pyautogui
import subprocess


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
        # Change the background color of the frame and buttons back to the default color when Shift key is released
        self.shift_pressed = False  # Set the shift_pressed flag to False
        for button in self.buttons:
            if button["text"] == "Log":
                button.config(bg="#3f4699")  # Set the background color of the "Log" button to a different color
            else:
                button.config(bg="#3f4652")  # Set the background color of other buttons to the default color


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
        self.create_button(name="miw", bg="#3f4652")  # Set the background color of the button to black
        self.create_button(name="media", bg="#3f4652")  # Set the background color of the button to black


        # # Create buttons with numbers 2 to 6
        # for index in range(2, 7):
        #     self.create_button(name=str(index), bg="#3f4652")  # Set the background color of the button to black

    def create_button(self, name="", padx=5, bg="#3f4652"):
        # Determine the index of the button in the list
        index = len(self.buttons) + 1

        # Set the text based on the index and name
        if (index in [1,2,3,4,5,6,7] and name):
            text = name
        else:
            text = str(index)

        # Create a new button and add it to the button frame
        button = tk.Button(
            self.button_frame,
            text=(" " + text + " ").center(padx),
            relief=tk.FLAT,  # Make the button flat
            bg=bg,  # Set the background color of the button
            fg="white"  # Set the text color to white
        )
        button.pack(side=tk.LEFT)

        # Bind left-click event to execute_shortcut method
        button.bind("<Button-1>", lambda event, idx=index: self.execute_shortcut(idx))

        # Bind right-click event to edit_button_text method
        button.bind("<Button-3>", lambda event, btn=button: self.edit_button_text(btn))

        # Bind shift + left-click event to execute_shift method
        # button.bind("<Shift-Button-1>", lambda event, idx=index: self.execute_shift(idx))
        button.bind("<Shift-Button-1>", lambda event, idx=index: (print(idx), self.execute_shift(idx)))
        # button.bind("<Shift-Button-1>", lambda event, idx=index: self.execute_shift(event, idx))



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

    # def execute_shift(self, index):


    #     # Convert the index to a string
    #     index_str = str(index)

    def execute_shift(index):
        print("indexz: "+ index)
        ahk_script = r'"C:\Program Files\AutoHotkey\UX\AutoHotkeyUX.exe"'
        script_path = r'"shift_window.ahk"'

        # Run AutoHotkey script with the index as an argument
        subprocess.run([ahk_script, script_path, str(index)])


    # ddd

    def execute_shortcut(self, index):
        # Convert the index to a string
        index_str = str(index)

        # if self.shift_pressed:  # If the shift key is pressed
        #     # shift focus to last window
        #     pyautogui.keyDown('alt')
        #     pyautogui.keyDown('tab')
        #     pyautogui.keyUp('alt')
        #     pyautogui.keyUp('tab')
        #     # Simulate pressing the Win, Alt
        #     pyautogui.keyDown('win')
        #     pyautogui.keyDown('alt')
        #     # send function key and shift.
        #     pyautogui.keyDown('shift')
        #     pyautogui.press('f' + index_str)
        # else:
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


        # if self.shift_pressed:  # If the shift key is pressed
        #     pyautogui.keyUp('shift')
        #     pyautogui.keyUp('f' + index_str)

class ShortcutButtonRow2(tk.Frame):
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
            button.config(bg="#007700")  # Set the background color of buttons to red

    def on_shift_key_release(self, event):
        # Change the background color of the frame and buttons back to the default color when Shift key is released
        self.shift_pressed = False  # Set the shift_pressed flag to False
        for button in self.buttons:
            if button["text"] == "Log":
                button.config(bg="#3f4699")  # Set the background color of the "Log" button to a different color
            else:
                button.config(bg="#3f4652")  # Set the background color of other buttons to the default color


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
        self.create_button(name="miw", bg="#3f4652")  # Set the background color of the button to black
        self.create_button(name="media", bg="#3f4652")  # Set the background color of the button to black


        # # Create buttons with numbers 2 to 6
        # for index in range(2, 7):
        #     self.create_button(name=str(index), bg="#3f4652")  # Set the background color of the button to black

    def create_button(self, name="", padx=5, bg="#3f4652"):
        # Determine the index of the button in the list
        index = len(self.buttons) + 1

        # Set the text based on the index and name
        if (index in [1,2,3,4,5,6,7] and name):
            text = name
        else:
            text = str(index)

        # Create a new button and add it to the button frame
        button = tk.Button(
            self.button_frame,
            text=(" " + text + " ").center(padx),
            relief=tk.FLAT,  # Make the button flat
            bg=bg,  # Set the background color of the button
            fg="white"  # Set the text color to white
        )
        button.pack(side=tk.LEFT)

        # Bind left-click event to execute_shortcut method
        button.bind("<Button-1>", lambda event, idx=index: self.execute_shortcut2(idx))

        # Bind right-click event to edit_button_text method
        button.bind("<Button-3>", lambda event, btn=button: self.edit_button_text(btn))

        # Bind shift + left-click event to execute_shift method
        # button.bind("<Shift-Button-1>", lambda event, idx=index: self.execute_shift(idx))
        button.bind("<Shift-Button-1>", lambda event, idx=index: (print(idx), self.execute_shift(idx)))
        # button.bind("<Shift-Button-1>", lambda event, idx=index: self.execute_shift(event, idx))



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

    def execute_shift(index):
        print("indexz: "+ index)
        ahk_script = r'"C:\Program Files\AutoHotkey\UX\AutoHotkeyUX.exe"'
        script_path = r'"shift_window.ahk"'

        # Run AutoHotkey script with the index as an argument
        subprocess.run([ahk_script, script_path, str(index)])

    def execute_shortcut2(self, index):


        pyautogui.hotkey('win', 'tab')
        print('bruh')
        time.sleep(0.1)
        # Convert the index to a string
        index_str = str(index)
        pyautogui.keyDown('win')
        pyautogui.keyDown('alt')
        pyautogui.keyDown('shift')

        # Simulate pressing the function key
        pyautogui.keyDown('f' + index_str)

        # Simulate releasing the function key
        pyautogui.keyUp('f' + index_str)

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
        button.config(bg="#3f4652")  # Set the background color of buttons to the default colo

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

# Calculate the width of the root window
width = root.winfo_screenwidth()


# Create the framey frame
framey = tk.Frame(root, bg="#1e2127")
framey.pack(side='right', padx=3, pady=3, fill=tk.Y, expand=True)

row = ShortcutButtonRow(framey)
row.grid(row=0, column=0)

row2 = ShortcutButtonRow2(framey)
row2.grid(row=1, column=0)


# Bind Shift key press and release events to change the background color of framey frame
# root.bind_all("<Shift-Key>", on_shift_key_press)
# root.bind_all("<KeyRelease-Shift_L>", on_shift_key_release)

root.bind_all("<Control-Key>", on_shift_key_press)
root.bind_all("<KeyRelease-Control_L>", on_shift_key_release)





root.bind("<Key>", on_key_press)
root.bind('<Control-Up>', handle_ctrl_up)
root.bind('<Control-Down>', handle_ctrl_down)


root.mainloop()