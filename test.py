import pyautogui
from time import sleep

sleep(3)


for x in range(50):
    pyautogui.press("home")
    pyautogui.write("the ")
    pyautogui.press("down")
    pyautogui.press("down")
