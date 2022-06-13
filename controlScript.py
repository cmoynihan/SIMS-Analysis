import pyautogui
import pandas as pd
from tkinter import messagebox
import readDepth

def readClicks(clickfile):
    clicks = pd.read_csv(clickfile, names=['x','y', 'button'])
    for index, row in clicks.iterrows():
        if row['button'] == 'Button.left':
            pyautogui.click(row['x'], row['y'])
        elif row['button'] == 'Button.right':
            pyautogui.rightClick(row['x'], row['y'])

def clearEntry():
    pyautogui.PAUSE = 0
    for i in range(10):
        pyautogui.hotkey('backspace')
    pyautogui.PAUSE = pauseTime

if __name__ == '__main__':
    pauseTime = 0.1
    data = readDepth.readDepth('Depth.txt')
    species = ['Total_Ion', 'Fe', 'Ni', 'Cr']
    pyautogui.PAUSE = pauseTime
    proceed = messagebox.askokcancel(title="Proceed?", message="Would you like to proceed?")
    if proceed:
        readClicks('selectWinCadence.csv')
        for time in data['Time Window']:
            readClicks('sequence1.csv') #sequence 1 clears all images, then begins the AcqSetup time window
            clearEntry()                #clear the box for the first time window entry
            pyautogui.typewrite(str(time[0])) #enter the first time that was read from the Depth.txt file
            readClicks('sequence2.csv') #select the second box
            clearEntry()                #clear the box for the second time window entry
            pyautogui.typewrite(str(time[1])) #enter the second time that was read from the Depth.txt file
            pyautogui.PAUSE = 1
            readClicks('sequence3.csv')
            pyautogui.PAUSE = pauseTime
            for i in range(4): #save image data
                name = f'{time[0]}s-{time[1]}s_{species[i]}'
                readClicks('sequence4.csv')
                clearEntry()
                pyautogui.typewrite(name + '.dat')
                pyautogui.hotkey('enter')
                pyautogui.hotkey('down')