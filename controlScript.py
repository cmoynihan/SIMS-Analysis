from tkinter import messagebox
import os
import time
import pandas as pd
import pyautogui
import readDepth

def readClicks(clickfile): #! this code feels repeated from exporter but maybe I am wrong
    clicklist = pd.read_csv(os.path.join('clickSequences', clickfile), names=['x','y', 'button'])
    textInstance = 0 # counter that logs which text instance the script is
    # iterate through the rows of the dataframe to extract click locations
    for index, row in clicklist.iterrows():
        if row['x'] != 'Text':
            # left or right click based on input
            pos = tuple((row['x'], row['y']))
            # if row['button'] == 'Button.left':
            #     pyautogui.click(pos)
            # elif row['button'] == 'Button.right':First text entryFirst text entryFirst text entryFirst text entryFirst text entry
            #     pyautogui.rightClick(pos)
        else:
            print(pos)
            inputText(textInstance)
            clearEntry(pos)
            textInstance += 1

def clearEntry(entryLocation): #! seems to work sometimes. What about a double click backspace or a click, shift, start kinda thing
    pyautogui.doubleClick(entryLocation)
    pyautogui.doubleClick(entryLocation)
    pyautogui.hotkey('backspace')

# put in your text here
def inputText(textInstance):
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
    # pauseTime = 0.1
    # data = readDepth.readDepth('Depth.txt')
    # species = ['Total_Ion', 'Fe', 'Ni', 'Cr']
    # pyautogui.PAUSE = pauseTime
    # proceed = messagebox.askokcancel(title="Proceed?", message="Would you like to proceed?") #! why would they not if they ran this script?
    # if proceed:
    #     readClicks('selectWinCadence.csv')
    #     for time in data['Time Window']:
    #         readClicks('sequence1.csv') #sequence 1 clears all images, then begins the AcqSetup time window
    #         clearEntry()                #clear the box for the first time window entry
    #         pyautogui.typewrite(str(time[0])) #enter the first time that was read from the Depth.txt file
    #         readClicks('sequence2.csv') #select the second box
    #         clearEntry()                #clear the box for the second time window entry
    #         pyautogui.typewrite(str(time[1])) #enter the second time that was read from the Depth.txt file
    #         pyautogui.PAUSE = 1
    #         readClicks('sequence3.csv')
    #         pyautogui.PAUSE = pauseTime
    #         for i in range(4): #save image data
    #             name = f'{time[0]}s-{time[1]}s_{species[i]}_image' # I would rather it be `iteration_species.dat`
    #             readClicks('sequence4.csv')
    #             clearEntry()
    #             pyautogui.typewrite(name + '.dat')
    #             pyautogui.hotkey('enter')
    #             pyautogui.hotkey('down')
