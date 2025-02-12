from pynput.keyboard import Listener
import pynput
import pyautogui as pg
pg.useImageNotFoundException(False)
import keyboard
import constants
import actions

# def on_press(key):
#     try:
#         print(f'Tecla pressionada: {key.char}')
#     except AttributeError:
#         print(f'Tecla especial pressionada: {key}')

# # Inicia o listener do teclado
# with Listener(on_press=on_press) as listener:
#     listener.join()



# def monster_out_of_range():
#     monster_out_of_range_box_top_region = pg.locateOnScreen('imgs/monster_target_out_of_range.png', confidence=0.8, region=constants.TOP_VIEW_REGION)
#     monster_out_of_range_box_left_region = pg.locateOnScreen('imgs/monster_target_out_of_range.png', confidence=0.8, region=constants.LEFT_VIEW_REGION)
#     monster_out_of_range_box_right_region = pg.locateOnScreen('imgs/monster_target_out_of_range.png', confidence=0.8, region=constants.RIGHT_VIEW_REGION)
#     monster_out_of_range_box_bottom_region = pg.locateOnScreen('imgs/monster_target_out_of_range.png', confidence=0.8, region=constants.BOTTOM_VIEW_REGION)
#     if monster_out_of_range_box_top_region or monster_out_of_range_box_left_region or monster_out_of_range_box_right_region or monster_out_of_range_box_bottom_region:
#         print('monstro fora da range')
#         print(monster_out_of_range_box_top_region, monster_out_of_range_box_left_region, monster_out_of_range_box_right_region, monster_out_of_range_box_bottom_region)
#         return True
#     else:
#         return False

# while True:
#     keyboard.wait('h')
#     monster_out_of_range()

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

while True:
    keyboard.wait('h')
    monster_out_of_range()