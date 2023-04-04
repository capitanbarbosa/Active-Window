
#
# ----------------------------------- Window creation (View) --------------------------------------
#

import tkinter as tk
from tkinter import ttk


def window():
    root = tk.Tk()

    overrideredirect_enabled = True

    # Remove title bar
    root.overrideredirect(True)

    # Set the window to always be on top
    root.wm_attributes("-topmost", True)

    # Set the window size
    root.geometry("1081x70+0+1370")

    # Set the title of the window
    root.title("Active Window 🚀🌙⭐")

    root.config(borderwidth=0)
    root.configure(background="#1e2127")
    root.config(borderwidth=0, bg="#1e2127")

    # Calculate the width of the root window
    width = root.winfo_screenwidth()

    # Create a function to round the edges of buttons
    # estilo universal de botones.... *****

    def round_button(widget):
        widget.config(relief="flat", borderwidth=1, highlightthickness=1)
        widget.config(bg="#1e2127", fg="#FFFFFF", activebackground="#1e2127")
        widget.config(highlightbackground="white", highlightcolor="white")
        widget.config(bd=2, padx=5, pady=0, font=(
            "Arial", 9), width=6, height=2)
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

    # ============ Create frame to hold Right - buttons
    frame = tk.Frame(root, bg="#1e2127")
    frame.pack(side='right', padx=0)
    # Configure column widths
    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=2)
    frame.columnconfigure(2, weight=2)

    # Create add-plus button
    plus_button = tk.Button(
        frame, text="+", command=lambda: createPage(databaseId, headers))
    round_button(plus_button)
    plus_button.grid(row=0, column=0, padx=0, pady=0)

    # Create update page button a1
    a1_button = tk.Button(frame, text="💾", command=update_database)
    round_button(a1_button)
    a1_button.grid(row=1, column=0, padx=0, pady=0)

    # Create toggle size button
    current_size = "1069x21"
    size_button = tk.Button(frame, text="⬛", command=toggle_size)
    round_button(size_button)
    size_button.grid(row=0, column=2, padx=0, pady=0)

    # Create move/lock button
    move_button = tk.Button(frame, text="🔒", command=move_lock)
    round_button(move_button)
    move_button.grid(row=1, column=2, padx=0, pady=0)

    # Create pomodoro button
    pomodoro_button = tk.Button(frame, text="⏰", command=toggle_timer)
    round_button(pomodoro_button)
    pomodoro_button.grid(row=0, column=1, padx=0, pady=0)

    root.bind("<Key>", on_key_press)
    root.bind('<Control-Up>', handle_ctrl_up)
    root.bind('<Control-Down>', handle_ctrl_down)

    # Create magic button a2
    a2_button = tk.Button(frame, text="🪄")
    round_button(a2_button)
    a2_button.grid(row=1, column=1, padx=0, pady=0)

    # ====== Create frame to hold Left navigation - buttons
    frameL = tk.Frame(root, bg="#1e2127")
    frameL.pack(side='right', padx=0)
    arrow_buttons_bg = "#3f4652"

    # Create button ↑ Next
    a3_button = tk.Button(frameL, text="↑", command=lambda: show_prev(current_project),
                          font=('TkDefaultFont', 14, 'bold'), width=2, height=1, bg=arrow_buttons_bg, relief="flat")
    a3_button.grid(row=0, column=0, padx=1, pady=0, sticky="nswe")

    # Create button ↓ Prev -  ← ↑ → ↓ ↚ ↛ ↜ ↝ ↞ ↟
    a4_button = tk.Button(frameL, text="↓", command=lambda: show_next(current_project),
                          font=('TkDefaultFont', 14, 'bold'), width=2, height=1, bg=arrow_buttons_bg, relief="flat")
    a4_button.grid(row=1, column=0, padx=1, pady=0, sticky="nswe")

    #
    # ------------------------------ input_box, paned_window to hold props_box, options_box
    #

    # -------------------------- frame input + checkbox
    # Create a frame to hold the checkbox and the input box
    checkbox_frame = tk.Frame(root, bg="#1e2127")
    checkbox_frame.pack(fill='both', expand=True)

    # Set the frame's background color to match the input box's background color
    checkbox_frame.config(borderwidth=0, bg="#1e2127")

    # Create the checkbox
    checkbox = tk.Checkbutton(
        checkbox_frame, bg="#1e2127", highlightthickness=0)

    # Add the checkbox to the frame
    checkbox.pack(side='right')

    # Set the checkbox's background color to match the input box's background color
    checkbox.config(bg="#1e2127")

    # Create a variable to hold the state of the checkbox
    checkbox.var = tk.IntVar()

    # Set the initial state of the checkbox to unchecked
    checkbox.var.set(0)

    # Bind the checkbox to the callback function
    checkbox.config(variable=checkbox.var, command=update_database)

    # Create the input box with 90% width
    input_box = tk.Text(checkbox_frame, height=1, width=int(
        width*0.9/7), bg="#1e2127", fg="white")

    # Add placeholder text
    input_box.insert('1.0', f"🪶 Active Log --> {name}\n")

    # Set cursor color to white
    input_box.config(insertbackground='white')

    # Add the input box to the frame
    input_box.pack(side='left', fill='both', expand=True)

    # Pack the checkbox_frame instead of the input box
    checkbox_frame.pack(fill='both', expand=True)
    # -----------------------------------------------------------------

    # Create paned window to hold note and options columns
    paned_window = tk.PanedWindow(
        root, orient=tk.HORIZONTAL, sashwidth=5, sashpad=5, showhandle=True, handlesize=10, bg=arrow_buttons_bg, bd=2)
    paned_window.pack(fill='both', expand=True, padx=1, pady=1)

    # Create Note column
    props_box = tk.Text(paned_window, height=3.7, width=118,
                        bg="#1e2127", fg="white")
    props_box.pack(fill='both', expand=True)

    # Add placeholder text
    props_box.insert('1.0', f"📝 Note --> {note}\n")

    # Set cursor color to white
    props_box.config(insertbackground='white')

    # Create options column
    options_box = tk.Text(paned_window, height=1.5, width=10,
                          bg="#1e2127", fg="white")
    options_box.pack(fill='both', expand=True)

    # Create a frame to hold the new button
    button_frame = tk.Frame(options_box, bg="#1e2127")
    button_frame.pack(side='left', padx=5)

    # Create the new button with updated text
    project_text = current_project if current_project != "" else "No Project"
    project_button = tk.Button(button_frame, text=project_text,
                               command=lambda: menu.post(project_button.winfo_rootx(), project_button.winfo_rooty()))
    project_button.config(width=130, height=4, bg=arrow_buttons_bg,
                          fg="white", activebackground="#1e2127")
    project_button.pack(side='left')

    # Create the dropdown menu
    menu = tk.Menu(project_button, tearoff=0)

    # Add the projects to the dropdown menu
    # pareciera que cada projecto lo vuelven un boton con el commando select_project y fija ese.
    # ese es el valor con el que hay que actualiozar el current_project q no aaparece el malvado...
    for project in projects:
        menu.add_command(
            label=project, command=lambda p=project: select_project(p))

    # Create the new button2
    new_button2 = tk.Button(button_frame, text="add/edit Tags",
                            command=lambda: print("New Button Clicked!"))
    new_button2.config(width=10, height=1, bg=arrow_buttons_bg,
                       fg="white", activebackground="#1e2127")
    new_button2.pack(side='left')

    # Create the new button3
    new_button3 = tk.Button(button_frame, text="link to note/task",
                            command=lambda: print("New Button Clicked!"))
    new_button3.config(width=10, height=1, bg=arrow_buttons_bg,
                       fg="white", activebackground="#1e2127")
    new_button3.pack(side='left')

    # Create the new button4
    new_button4 = tk.Button(button_frame, text="wiz commands",
                            command=lambda: print("New Button Clicked!"))
    new_button4.config(width=10, height=1, bg=arrow_buttons_bg,
                       fg="white", activebackground="#1e2127")
    new_button4.pack(side='left')

    # Add columns to paned window
    paned_window.add(props_box)
    paned_window.add(options_box)

    # Read the database and show the first result
    readDatabase(databaseId)
    # show_result(current_index, project)

    root.mainloop()
