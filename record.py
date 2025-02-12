import pyautogui as pg
from pynput.keyboard import Listener
from pynput import keyboard
import os
import json
import constants

# Function to create a folder if it does not exist
def create_folder():
    if not os.path.isdir(constants.FOLDER_NAME):  # Checks if the folder exists
        os.mkdir(constants.FOLDER_NAME)  # Creates the folder if it doesn't exist

# Class to record and manage coordinates for in-game navigation
class Rec:
    def __init__(self):
        create_folder()  # Ensures the folder is created
        self.count = 0  # Counter for saved screenshots
        self.coordinates = []  # List to store coordinate information

    # Takes a screenshot of the cursor position and saves it
    def photo(self):
        x, y = pg.position()  # Gets the current mouse position
        photo = pg.screenshot(region=(x - 5, y - 5, 12, 12))  # Captures a small region around the cursor
        path = f'{constants.FOLDER_NAME}/flag_{self.count}.png'  # Defines the file path for the screenshot
        photo.save(path)  # Saves the screenshot
        self.count += 1  # Increments the screenshot counter
        infos = {
            "path": path,  # Path to the saved screenshot
            "down_hole": 0,  # Indicates whether a hole down action is needed
            "up_hole": 0,  # Indicates whether a hole up action is needed
            "wait": 10  # Default wait time before the next action
        }
        self.coordinates.append(infos)  # Adds the captured information to the list

    # Marks the last recorded coordinate as a hole-down location
    def down_hole(self):
        last_coordinates = self.coordinates[-1]  # Gets the last recorded coordinate
        last_coordinates['down_hole'] = 1  # Updates the flag indicating a hole down action

    # Marks the last recorded coordinate as a hole-up location
    def up_hole(self):
        last_coordinates = self.coordinates[-1]  # Gets the last recorded coordinate
        last_coordinates['up_hole'] = 1  # Updates the flag indicating a hole up action

    # Handles key press events to trigger different actions
    def key_code(self, key):
        if key == keyboard.Key.esc:  # If ESC is pressed, save data and stop recording
            with open(f'{constants.FOLDER_NAME}/infos.json', 'w') as file:
                file.write(json.dumps(self.coordinates))  # Saves recorded coordinates as a JSON file
            return False  # Stops the key listener
        if key == keyboard.Key.insert:  # If INSERT is pressed, take a screenshot
            self.photo()
        
