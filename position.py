import tkinter as tk

root = tk.Tk()

# Get the number of available screens
num_screens = root.get_num_screens()

# Check if a secondary screen is available
if num_screens > 1:
    # Get the dimensions of the secondary screen (index 1)
    secondary_screen_width = root.winfo_screenwidth(1)
    secondary_screen_height = root.winfo_screenheight(1)

    # Create and position the secondary window
    secondary_window = tk.Toplevel(root)
    secondary_window.geometry(f"{desired_width}x{desired_height}+0+{secondary_screen_height}")
    # ... Configure and pack widgets for the secondary window ...

root.mainloop()
