from tkinter import messagebox
import os
import time
import pandas as pd
import pyautogui

def readClicks(clickfile):
    '''
    readClicks()
    Reads a .csv file exported by recorderGUI.py and performs a series of clicks and
    text entries.

    Input:
    clickfile - a .csv file containing click locations and text markers

    No outputs
    '''
    clicklist = pd.read_csv(os.path.join('clickSequences', clickfile), names=['x','y', 'button'])
    textInstance = 0 # counter that logs which text instance the script is
    # iterate through the rows of the dataframe to extract click locations
    for index, row in clicklist.iterrows():
        if row['x'] != 'Text':
            # left or right click based on input
            pos = tuple((row['x'], row['y']))
            if row['button'] == 'Button.left':
                pyautogui.click(pos)
            elif row['button'] == 'Button.right':
                pyautogui.rightClick(pos)
        else:
            inputText(textInstance)
            clearEntry(pos)
            textInstance += 1

def clearEntry(entryLocation):
    '''
    clearEntry()
    Double clicks twice on a entryLocation (twice is necessary to modify excel spreadsheets) 
    to select all of the text in the box located at entry location, the presses backspace.

    Inputs:
    entryLocation - A tuple representing the x and y coordinates of the text box.

    No outputs
    '''
    pyautogui.doubleClick(entryLocation)
    pyautogui.doubleClick(entryLocation)
    pyautogui.hotkey('backspace')

# put in your text here
def inputText(textInstance):
    '''
    inputText()
    Writes text into a text box, can write different messages based on the input.

    Inputs:
    textInstance - The text instance number for a given text box. Allows different
                   text to be entered based on the entry number.
    '''
    if textInstance == 0:
        pyautogui.write('First text entry')
    elif textInstance == 1:
        pyautogui.write('Second text entry')
    elif textInstance == 2:
        pyautogui.write('Third text entry')
    elif textInstance == 3:
        pyautogui.write('Fourth text entry')

if __name__ == '__main__':
    time.sleep(2)
    pyautogui.PAUSE = 1
    readClicks('paintyBoi.csv')

