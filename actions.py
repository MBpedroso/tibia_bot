import pyautogui as pg
import constants
import keyboard

# Function to check if a battle is active by detecting the battle interface on the screen
def get_battle():
    return pg.locateOnScreen('imgs/battle.PNG', confidence=0.9)

# Function to move the character down through a hole if required
def hole_down(should_down):
    if should_down:
        box = pg.locateOnScreen('imgs/hole_down.png', confidence=0.8)  # Searches for the hole image on screen
        if box:
            x, y = pg.center(box)  # Gets the center coordinates of the detected hole
            pg.moveTo(x, y)  # Moves the cursor to the hole position
            pg.click()  # Clicks to move down

# Function to move the character up through a hole if required
def hole_up(should_up, img_anchor, plus_x, plus_y):
    if should_up:
        box = pg.locateOnScreen(img_anchor, confidence=0.8)  # Searches for the anchor image indicating the hole location
        if box:
            x, y = pg.center(box)  # Gets the center coordinates of the detected anchor
            pg.moveTo(x + plus_x, y + plus_y)  # Adjusts the movement position with additional x and y offsets
            pg.press('f5')  # Presses a key (F5) before clicking (possibly to use a rope or ladder)
            pg.click()  # Clicks to move up
            pg.sleep(2)  # Waits for the movement to complete

# Function to check if the player is anchored at a specific location
def check_anchor():
    box = pg.locateOnScreen('imgs/anchor.png', confidence=0.8)  # Searches for the anchor image
    if box:
        pg.moveTo(1895, 10)  # Moves the cursor to a specific screen position (possibly UI interaction)
        pg.click()
        pg.moveTo(1111, 587)  # Moves to another UI position
        pg.click()
        return False  # Indicates that the player is anchored
    return True  # Indicates that the player is not anchored

# Function to check the player's status and take action based on health or mana levels
def check_status(name, delay, x, y, rgb, button_name):
    print(f'Checking {name}')
    pg.sleep(delay)  # Waits before checking the status
    if pg.pixelMatchesColor(x, y, rgb):  # Compares the color of a specific screen pixel
        pg.press(button_name)  # Presses the corresponding key (e.g., healing or mana regeneration)

# Function to make the character eat food
def eat_food():
    pg.press('F6')  # Presses F6 (likely assigned to a food item)
    print('Eating food')
