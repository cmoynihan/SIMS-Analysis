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
    pyautogui.PAUSE = 0.5
    depth = readDepth.readDepth('Depth.txt')
    imageFolder = os.path.join('C:\\','Users','Fusion','Documents','SIMS-Analysis','WinCadence_Reader','Data','Images')
    # cr.readClicks(os.path.join('.', 'clickSequences', 'test1.csv'), [], [])
    cr.readClicks(os.path.join('.', 'click_recorder_package', 'clickSequences', 'winCadence1.csv'), [str(depth['Time Window'][0][0]), str(depth['Time Window'][0][1])] + [os.path.join(imageFolder, 'save1.dat'), 'down', os.path.join(imageFolder,'save2.dat')], [2])
    # print(depth['Time Window'][0])