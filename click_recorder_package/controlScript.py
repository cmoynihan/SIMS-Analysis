from tkinter import messagebox
import os
import time
import pandas as pd
import pyautogui

def readClicks(clickfile, textList, loopLengths):
    '''
    readClicks()
    Reads a .csv file exported by recorderGUI.py and performs a series of clicks and
    text entries.

    Input:
    clickfile - a .csv file containing click locations and text markers
    textList - list of all text inputs that will be needed
    loopLengths - list of the length of all loops in chronological order

    No outputs
    '''
    clicklist = pd.read_csv(os.path.join('clickSequences', clickfile), names=['x','y', 'button'])
    textInstance = 0 # counter that logs which text instance the script is
    sections = getLoops(clicklist) # break the clicklist up into sections based on where the loops begin and end
    # iterate through the rows of the dataframe to extract click locations
    for i in range(len(sections)):
        if i % 2 == 1:
            for j in range(loopLengths[int(i / 2)]):
                for index, row in sections[i].iterrows():
                    if row['x'] != 'Text':
                        # left or right click based on input
                        pos = tuple((row['x'], row['y']))
                        if row['button'] == 'Button.left':
                            pyautogui.click(pos)
                        elif row['button'] == 'Button.right':
                            pyautogui.rightClick(pos)
                    else:
                        clearEntry(pos)
                        inputText(textList[textInstance])
                        textInstance += 1
        else:
            for index, row in sections[i].iterrows():
                    if row['x'] != 'Text':
                        print(tuple((row['x'], row['y'], row['button'])))
                        # left or right click based on input
                        pos = tuple((row['x'], row['y']))
                        if row['button'] == 'Button.left':
                            pyautogui.click(pos)
                        elif row['button'] == 'Button.right':
                            pyautogui.rightClick(pos)
                    else:
                        clearEntry(pos)
                        inputText(textList[textInstance])
                        textInstance += 1
            

def getLoops(clicklist):
    '''
    getLoops()
    Takes clicklist and breaks it into a set of dataFrames, based on the location of the
    'Loop' entries in the clicklist

    Input:
    clicklist - a Pandas DataFrame that stores the click recording information
    Output:
    sections - a list of Pandas DataFrames corresponding to each loop section. 
               Odd-indexed sections correspond to loops.
    '''
    sections = [] #list of dataFrames to store each section of the clicklist
    begin = 0
    for index, row in clicklist.iterrows():
        if row['x'] == 'Loop':
            sections.append(clicklist[begin:index])
            begin = index + 1
    return sections

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
    # read first entry to list
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
    readClicks('testLoop2.csv', ['2','jdk'], [2, 2])
