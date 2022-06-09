from asyncore import read
from msilib import sequence
import pyautogui
import pandas as pd

def readClicks(clickfile):
    clicks = pd.read_csv(clickfile, names=['x','y'])
    for index, row in clicks.iterrows():
        pyautogui.click(row['x'], row['y'])

def clearEntry():
    for i in range(10):
        pyautogui.hotkey('backspace')

if __name__ == '__main__':
    readClicks('sequence1.csv')
    clearEntry()
    readClicks('sequence2.csv')
    clearEntry()