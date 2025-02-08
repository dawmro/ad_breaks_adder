import pyautogui
import time
import json
from pynput import keyboard

# Initialize variables to store coordinates
coordinates = {
    "ad_break_button": None,
    "ad_begin_timeline": None,
    "ad_end_timeline": None
}

def on_press(key):
    global coordinates
    try:
        if key.char == '1':  # Pressing the '1' key
            coordinates["ad_break_button"] = pyautogui.position()
            print(f"Ad break button coordinates: x={coordinates['ad_break_button'][0]}, y={coordinates['ad_break_button'][1]}")
        elif key.char == '2':  # Pressing the '2' key
            coordinates["ad_begin_timeline"] = pyautogui.position()
            print(f"Ad begin timeline coordinates: x={coordinates['ad_begin_timeline'][0]}, y={coordinates['ad_begin_timeline'][1]}")
        elif key.char == '3':  # Pressing the '3' key
            coordinates["ad_end_timeline"] = pyautogui.position()
            print(f"Ad end timeline coordinates: x={coordinates['ad_end_timeline'][0]}, y={coordinates['ad_end_timeline'][1]}")
    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.esc:  # Pressing the 'Esc' key to stop the listener
        return False

def save_coordinates_to_file(coordinates, filename):
    with open(filename, 'w') as file:
        json.dump(coordinates, file, indent=4)

def load_coordinates_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def get_mouse_position():
    """
    Continuously prints the current mouse position every second.
    """
    global coordinates
    filename = "coordinates.json"
    existing_coordinates = load_coordinates_from_file(filename)
    if existing_coordinates:
        coordinates = existing_coordinates
        print("Loaded existing coordinates:")
        print(coordinates)

    try:
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()
        while True:
            print(pyautogui.position())
            time.sleep(1)
    except KeyboardInterrupt:  # Ctrl + C
        listener.stop()
        print("Mouse position tracking stopped.")
        print("Final coordinates:")
        print(coordinates)
        save_coordinates_to_file(coordinates, filename)
        print(f"Coordinates saved to {filename}")


if __name__ == "__main__":
	get_mouse_position()