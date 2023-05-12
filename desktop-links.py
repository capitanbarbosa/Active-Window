import tkinter as tk
import pyautogui

class ShortcutButtonRow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.buttons = []
        self.create_widgets()

    def create_widgets(self):
        # Create a frame to hold the buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.LEFT)

        # Create the initial buttons
        self.create_button()

        # Create the "+" button to add more buttons
        self.add_button = tk.Button(self, text="+", command=self.create_button)
        self.add_button.pack(side=tk.LEFT)

    def create_button(self):
        # Determine the index of the button in the list
        index = len(self.buttons) + 1

        # Create a new button and add it to the button frame
        button = tk.Button(self.button_frame, text="Shortcut {}".format(index),
                           command=lambda idx=index: self.execute_shortcut(idx))
        button.pack(side=tk.LEFT)

        # Add the button to the list
        self.buttons.append(button)

    def execute_shortcut(self, index):
        # Convert the index to a string
        index_str = str(index)

        # Simulate pressing the Win, Alt, and Shift keys
        pyautogui.keyDown('win')
        pyautogui.keyDown('alt')
        pyautogui.keyDown('shift')

        # Simulate pressing the index key
        pyautogui.press(index_str)

        # Simulate releasing the Win, Alt, Shift, and index keys
        pyautogui.keyUp('win')
        pyautogui.keyUp('alt')
        pyautogui.keyUp('shift')
        pyautogui.keyUp(index_str)

# Create the main window
root = tk.Tk()

# Create the ShortcutButtonRow component
row = ShortcutButtonRow(root)
row.pack()

# Start the Tkinter event loop
root.mainloop()
