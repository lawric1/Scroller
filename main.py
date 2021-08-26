import pyautogui
import keyboard

speed = 0

try:
    while True:
        if keyboard.is_pressed('x'):
            speed -= 3
        elif keyboard.is_pressed('z'):
            speed += 3
        elif keyboard.is_pressed('ctrl'):
            speed = 0

        pyautogui.scroll(speed)
except KeyboardInterrupt:
    print('\n')