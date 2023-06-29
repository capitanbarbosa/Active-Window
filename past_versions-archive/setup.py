import ctypes

def get_virtual_desktop_names():
    user32 = ctypes.windll.user32
    virtual_desktops = []

    def enum_windows_callback(hwnd, lParam):
        title_length = user32.GetWindowTextLengthW(hwnd)
        title_buffer = ctypes.create_unicode_buffer(title_length + 1)
        user32.GetWindowTextW(hwnd, title_buffer, title_length + 1)
        title = title_buffer.value

        if title.startswith("Desktop"):
            virtual_desktops.append(title)

        return True

    user32.EnumWindows(ctypes.WNDENUMPROC(enum_windows_callback), 0)

    return virtual_desktops

virtual_desktops = get_virtual_desktop_names()
print(virtual_desktops)
