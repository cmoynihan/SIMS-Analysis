import pyautogui
import pandas as pd
import readDepth

def readClicks(clickfile):
    clicks = pd.read_csv(clickfile, names=['x','y', 'button'])
    for index, row in clicks.iterrows():
        if row['button'] == 'Button.left':
            pyautogui.click(row['x'], row['y'])
        elif row['button'] == 'Button.right':
            pyautogui.rightClick(row['x'], row['y'])

def clearEntry():
    for i in range(10):
        pyautogui.hotkey('backspace')

if __name__ == '__main__':
    data = readDepth.readDepth('Depth.txt')
    i = 0
    pyautogui.PAUSE = 0.2
    for time in data['Time Window']:
        if i == 0:
            readClicks('sequence1.csv') #sequence 1 clears all images, then begins the AcqSetup time window
            clearEntry()                #clear the box for the first time window entry
            pyautogui.typewrite(str(time[0])) #enter the first time that was read from the Depth.txt file
            readClicks('sequence2.csv') #select the second box
            clearEntry()                #clear the box for the second time window entry
            pyautogui.typewrite(str(time[1])) #enter the second time that was read from the Depth.txt file
            i = 1