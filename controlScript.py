from asyncore import read
from msilib import sequence
import pyautogui
import pandas as pd
import readDepth

def readClicks(clickfile):
    clicks = pd.read_csv(clickfile, names=['x','y'])
    for index, row in clicks.iterrows():
        pyautogui.click(row['x'], row['y'])

def clearEntry():
    for i in range(10):
        pyautogui.hotkey('backspace')

if __name__ == '__main__':
    data = readDepth.readDepth('Depth.txt')
    i = 0
    for time in data['Time Window']:
        if i == 0:
            readClicks('sequence1.csv')
            clearEntry()
            pyautogui.typewrite(str(time[0]))
            readClicks('sequence2.csv')
            clearEntry()
            pyautogui.typewrite(str(time[1]))
            i = 1