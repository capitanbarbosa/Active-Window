import pyautogui
import time

try:
    while True:
        # Get the current mouse position
        x, y = pyautogui.position()

        # Print the position
        print(f'Current mouse position: (x={x}, y={y})')

        # Wait for 3 seconds
        time.sleep(3)
except KeyboardInterrupt:
    print("Script terminated by user.")
