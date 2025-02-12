import pyautogui as pg
pg.useImageNotFoundException(False)
import keyboard
import actions
import constants
import json
from pynput.keyboard import Listener
from pynput import keyboard
import threading
import my_thread

           
def kill_monsters():             
    while actions.get_battle() == None:
        pg.press('space')
        print('killing monster')
        if event_th.is_set(): 
            return
        while pg.locateOnScreen('imgs/monster_red_target.png', confidence=0.8, region=constants.BATTLE_REGION, grayscale=False):
            if event_th.is_set():
                return 
            print('Wainting monster death')
            if monster_out_of_range():
                print('monstro fora da range')
                pg.press('space')


def monster_out_of_range():
    monster_out_of_range_box_top_region = pg.locateOnScreen('imgs/monster_target_out_of_range.png', confidence=0.9, region=constants.TOP_VIEW_REGION, grayscale=False)
    monster_out_of_range_box_left_region = pg.locateOnScreen('imgs/monster_target_out_of_range.png', confidence=0.9, region=constants.LEFT_VIEW_REGION, grayscale=False)
    monster_out_of_range_box_right_region = pg.locateOnScreen('imgs/monster_target_out_of_range.png', confidence=0.9, region=constants.RIGHT_VIEW_REGION, grayscale=False)
    monster_out_of_range_box_bottom_region = pg.locateOnScreen('imgs/monster_target_out_of_range.png', confidence=0.9, region=constants.BOTTOM_VIEW_REGION, grayscale=False)
    if monster_out_of_range_box_top_region or monster_out_of_range_box_left_region or monster_out_of_range_box_right_region or monster_out_of_range_box_bottom_region:
        print('monstro fora da range')
        print(monster_out_of_range_box_top_region, monster_out_of_range_box_left_region, monster_out_of_range_box_right_region, monster_out_of_range_box_bottom_region)
        return True
    else:
        return False

def get_loot():
    loot = pg.locateAllOnScreen('imgs/dead_monster.png', confidence=0.9, region=constants.LOOT_REGION)
    for box in loot:
        x, y = pg.center(box)
        pg.moveTo(x, y)
        pg.click(button='right')
        print('getting loot')

def go_to_flag(path, wait):
    flag = pg.locateOnScreen(path, confidence=0.8, region=constants.MAP_REGION, grayscale=False)
    if flag:
        x,y = pg.center(flag)
        if event_th.is_set():
            return
        pg.moveTo(x, y)
        if event_th.is_set():
            return
        pg.click()
        pg.sleep(wait)

def check_player_position():
    return pg.locateOnScreen('imgs/point_player.png', confidence=0.8, region=constants.MAP_REGION)


def run():
    with open(f'{constants.FOLDER_NAME}/infos.json', 'r') as file:
        data = json.loads(file.read())
    while True:
        for item in data:
            print(f'rodando para imagem: {item['path']}')
            if not actions.check_anchor():
                return
            if event_th.is_set():
                return
            kill_monsters()
            if event_th.is_set():
                return
            pg.sleep(1)
            get_loot()
            go_to_flag(item['path'], item['wait'])
            kill_monsters()
            pg.sleep(1)
            get_loot()
            if check_player_position():
                print('ainda nao chegou no destino.')
                kill_monsters()
                if event_th.is_set():
                    return
                pg.sleep(1)
                get_loot()
                if event_th.is_set():
                    return
                go_to_flag(item['path'], item['wait'])
            
            actions.eat_food()
            actions.hole_down(item['down_hole'])
            actions.hole_up(item['up_hole'], f'{constants.FOLDER_NAME}/anchor_floor_2.png', 400 , 0)
            actions.hole_up(item['up_hole'], f'{constants.FOLDER_NAME}/anchor_floor_3.png', 120 , 120)


def key_code(key, th_group):
    if key == keyboard.Key.esc:
        print('parou')
        event_th.set()
        th_group.stop()
        return False
    if key == keyboard.Key.delete:
        th_run.start()
        th_group.start()
    
global event_th
event_th = threading.Event()
th_run = threading.Thread(target=run)

th_full_mana = my_thread.MyThread(lambda: actions.check_status('mana', 5, *constants.POSITION_MANA_FULL, constants.COLOR_MANA, 'F3'))
th_check_life = my_thread.MyThread(lambda: actions.check_status('vida', 2, *constants.POSITION_LIFE, constants.COLOR_LIFE, 'F3'))

group_thread = my_thread.ThreadGroup([th_full_mana, th_check_life])

with Listener(on_press=lambda key: key_code(key, group_thread)) as listener:
    listener.join()

