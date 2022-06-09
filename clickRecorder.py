from tkinter.messagebox import YESNO
import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

screenWidth, screenHeight = pyautogui.size()

def write_clicks(clickArray, filename):
    with open(str(filename) + '.csv','w') as clickList:
        for click in clickArray[1:-2]:
            clickList.write(f'{click[0]},{click[1]}\n')


recording = False #False if the program is not recording to the click list, True if it

clicks = []
def on_click(x, y, button, pressed):
    if pressed and recording:
        clicks.append((x,y))