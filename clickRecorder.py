from tkinter.messagebox import YESNO
import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2

screenWidth, screenHeight = pyautogui.size()

def write_clicks(clickArray, filename):
    with open(str(filename),'w') as clickList:
        for click in clickArray[1:-2]:
            clickList.write(f'{click[0]},{click[1]},{click[2]}\n')


recording = False #False if the program is not recording to the click list, True if it is

clicks = []
def on_click(x, y, button, pressed):
    if pressed and recording:
        clicks.append((x,y, button))