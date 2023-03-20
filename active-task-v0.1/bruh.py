import win32gui
import win32con
import win32ui

# Load the default tkinter icon
hIcon = win32gui.LoadIcon(None, win32con.IDI_APPLICATION)

# Get the icon bitmap
hBitmap = win32gui.GetIconInfo(hIcon)[4]
bmp = win32ui.CreateBitmapFromHandle(hBitmap)

# Save the icon to a file
with open('tkinter_icon.ico', 'wb') as icon_file:
    bmp.SaveImageFile(icon_file, "ico")
