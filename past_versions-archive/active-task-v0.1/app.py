import tkinter as tk
from model import Model
from view import View
from controller import Controller

# Create the model
model = Model()

# Create the view
root = tk.Tk()
view = View(root)

# Create the controller
controller = Controller(model, view)

# Start the app
root.mainloop()
