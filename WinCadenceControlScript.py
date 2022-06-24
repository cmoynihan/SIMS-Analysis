from tkinter import messagebox
import os
import time
import pandas as pd
import pyautogui
import sys
import readDepth
import click_recorder_package as cr


if __name__ == '__main__':
    time.sleep(2)
    pyautogui.PAUSE = 2
    depth = readDepth.readDepth('Depth.txt')
    imageFolder = os.path.join('C:\\','Users','Fusion','Documents','SIMS-Analysis','WinCadence_Reader','Data','Images')
    # cr.readClicks(os.path.join('.', 'clickSequences', 'test1.csv'), [], [])
    elements = ['Total_ion', 'Fe', 'Cr', 'Ni']
    savenames = [0]*(2*len(elements) - 1)
    textList = []
    # for index, row in depth.iterrows():
    
    #     textList = textList + [str(depth['Time Window'][index][0]), str(depth['Time Window'][index][1])] + savenames
    # print(textList)
    for index, row in depth.iterrows():
        for i in range(len(elements)):
            savenames[2*i] = os.path.join(imageFolder, str(index) + '_' + elements[i] + '.dat')
            savenames[2*i - 1] = 'down'
        textList = [str(depth['Time Window'][index][0]), str(depth['Time Window'][index][1])] + savenames
        if index < 5:
            
            cr.readClicks(os.path.join('.', 'click_recorder_package', 'clickSequences', 'winCadence1.csv'), 
                textList, [len(elements)])
    # print(depth['Time Window'][0])