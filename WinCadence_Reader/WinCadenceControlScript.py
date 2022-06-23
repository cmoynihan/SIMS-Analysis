from tkinter import messagebox
import os
import time
import pandas as pd
import pyautogui
import controlScript
import readDepth as rd


if __name__ == '__main__':
    time.sleep(2)
    pyautogui.PAUSE = 1
    depth = rd.readDepth('Depth.txt')


