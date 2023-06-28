    def highlight_current_desktop(self):
        # Get the active virtual desktop
        active_desktop = VirtualDesktop.current()

        # Get the index of the active desktop
        active_desktop_index = active_desktop.number

        # Highlight the current desktop index button
        for index, button in enumerate(self.buttons, start=1):
            if str(index) == str(active_desktop_index):
                button.config(bg="#FF6904")  # Set the background color of the current desktop index button to pink
            else:
                button.config(bg="#3f4652")  # Set the background color of other buttons to the default color

        # Schedule the next update after 1 second (adjust the duration as desired)
        root.after(1000, self.highlight_current_desktop)
