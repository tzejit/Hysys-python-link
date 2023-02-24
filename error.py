from pynput.keyboard import Key, Controller
import time

def enter_press():
    keyboard = Controller()

    while True:
        time.sleep(5)
        keyboard.press(Key.enter)