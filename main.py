import pyautogui as pg
pg.useImageNotFoundException(False)  # Disables exception when an image is not found
import keyboard
import actions
import constants
import json
from pynput.keyboard import Listener
from pynput import keyboard
import threading
import my_thread

# Function to attack monsters
def kill_monsters():             
    while actions.get_battle() is None:  # Waits until a battle is detected
        pg.press('space')  # Presses space to attack
        print('killing monster')
        if event_th.is_set():  # Checks if the stop event is triggered
            return
        # While there is a monster target on the screen
        while pg.locateOnScreen('imgs/monster_red_target.png', confidence=0.8, region=constants.BATTLE_REGION, grayscale=False):
            if event_th.is_set():  # Checks again if the stop event is triggered
                return 
            print('Waiting for monster death')
            if monster_out_of_range():  # If the monster is out of range
                print('Monster out of range')
                pg.press('space')  # Tries to attack again

# Function to check if the monster is out of range
def monster_out_of_range():
    regions = {
        "top": constants.TOP_VIEW_REGION,
        "left": constants.LEFT_VIEW_REGION,
        "right": constants.RIGHT_VIEW_REGION,
        "bottom": constants.BOTTOM_VIEW_REGION
    }
    
    # Searches for the monster out-of-range image in each defined region
    detected_regions = {
        name: pg.locateOnScreen('imgs/monster_target_out_of_range.png', confidence=0.9, region=region, grayscale=False)
        for name, region in regions.items()
    }

    # If any region detects that the monster is out of range, return True
    if any(detected_regions.values()):
        print("Monster out of range:", detected_regions)
        return True
    return False

# Function to loot dead monsters
def get_loot():
    loot = pg.locateAllOnScreen('imgs/dead_monster.png', confidence=0.9, region=constants.LOOT_REGION)
    for box in loot:
        x, y = pg.center(box)  # Gets the central coordinates of the loot
        pg.moveTo(x, y)
        pg.click(button='right')  # Right-clicks to collect the loot
        print('getting loot')

# Function to move to a flag on the minimap
def go_to_flag(path, wait):
    flag = pg.locateOnScreen(path, confidence=0.8, region=constants.MAP_REGION, grayscale=False)
    if flag:
        x, y = pg.center(flag)
        if event_th.is_set():  # Checks if the stop event is triggered
            return
        pg.moveTo(x, y)
        if event_th.is_set():  # Checks again before clicking
            return
        pg.click()
        pg.sleep(wait)  # Waits for the movement to complete

# Function to check the player's position on the minimap
def check_player_position():
    return pg.locateOnScreen('imgs/point_player.png', confidence=0.8, region=constants.MAP_REGION)

# Main function that executes the bot's logic
def run():
    with open(f'{constants.FOLDER_NAME}/infos.json', 'r') as file:
        data = json.loads(file.read())  # Loads JSON data containing movement and action instructions
    while True:
        for item in data:
            print(f'Running for image: {item["path"]}')
            if not actions.check_anchor():  # Checks if the bot is still anchored in the right location
                return
            if event_th.is_set():  # Stops if the stop event is triggered
                return
            kill_monsters()  # Attacks monsters
            if event_th.is_set():
                return
            pg.sleep(1)
            get_loot()  # Collects loot
            go_to_flag(item['path'], item['wait'])  # Moves to the next flag location
            kill_monsters()
            pg.sleep(1)
            get_loot()
            if check_player_position():  # If the player has not reached the destination yet
                print('Still not at the destination.')
                kill_monsters()
                if event_th.is_set():
                    return
                pg.sleep(1)
                get_loot()
                if event_th.is_set():
                    return
                go_to_flag(item['path'], item['wait'])  # Attempts to move again
            
            # Executes food consumption and hole movements
            actions.eat_food()
            actions.hole_down(item['down_hole'])
            actions.hole_up(item['up_hole'], f'{constants.FOLDER_NAME}/anchor_floor_2.png', 400, 0)
            actions.hole_up(item['up_hole'], f'{constants.FOLDER_NAME}/anchor_floor_3.png', 120, 120)

# Function to handle keyboard inputs for starting and stopping the bot
def key_code(key, th_group):
    if key == keyboard.Key.esc:  # Stops the bot when ESC is pressed
        print('Stopped')
        event_th.set()
        th_group.stop()
        return False
    if key == keyboard.Key.delete:  # Starts the bot when DELETE is pressed
        th_run.start()
        th_group.start()

# Global event flag to stop threads
global event_th
event_th = threading.Event()
th_run = threading.Thread(target=run)

# Threads for checking health and mana status
th_full_mana = my_thread.MyThread(lambda: actions.check_status('mana', 5, *constants.POSITION_MANA_FULL, constants.COLOR_MANA, 'F3'))
th_check_life = my_thread.MyThread(lambda: actions.check_status('life', 2, *constants.POSITION_LIFE, constants.COLOR_LIFE, 'F3'))

# Grouping threads for better control
group_thread = my_thread.ThreadGroup([th_full_mana, th_check_life])

# Listens for keyboard input to control the bot
with Listener(on_press=lambda key: key_code(key, group_thread)) as listener:
    listener.join()
