import pyautogui as pg
import constants
import keyboard



def get_battle():
    return pg.locateOnScreen('imgs/battle.PNG',confidence=0.9)

def hole_down(should_down):
    if should_down:
        box = pg.locateOnScreen('imgs/hole_down.png', confidence = 0.8)
        if box:
            x, y = pg.center(box)
            pg.moveTo(x, y)
            pg.click()

def hole_up(should_up, img_anchor, plus_x, plus_y):
    if should_up:
        box = pg.locateOnScreen(img_anchor, confidence=0.8)
        if box:
            x, y = pg.center(box)
            pg.moveTo(x + plus_x, y + plus_y)
            pg.press('f5')
            pg.click()
            pg.sleep(2)

def check_anchor():
    box = pg.locateOnScreen('imgs/anchor.png', confidence=0.8)
    if box:
        pg.moveTo(1895, 10)
        pg.click()
        pg.moveTo(1111, 587)
        pg.click()
        return False
    return True

def check_status(name, delay, x, y, rgb, button_name):
    print(f'checando {name}')
    pg.sleep(delay)
    if pg.pixelMatchesColor(x, y, rgb):
        pg.press(button_name)


def eat_food():
    pg.press('F6')
    print('comendo comida')

