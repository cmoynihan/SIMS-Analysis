
import tkinter as tk  #! no blank lines at top of file
from tkinter import DISABLED, END, NORMAL, ttk
from tkinter import messagebox #! why a new line to import from the same package?
import pyautogui
import pandas as pd
from pynput import mouse
import os  #! packages in the standard python library should be imported before third party packages

#! FAILSAFE is True by default. I probably would not give the user the option to turn it off by including it 
pyautogui.FAILSAFE = True #DO NOT TURN OFF!! FAILSAFE allows the user to terminate the program by mousing up to the top left of the screen.
pyautogui.PAUSE = 1 #delay (in seconds) between pyautogui calls
recording = False #False if the program is not recording to the click list, True if it is
clicks = [] #list to temporarily store locations of clicks during recording
screenWidth, screenHeight = pyautogui.size() #! this is never used again, why is it needed?

#GUI window class
class exporterGUI(tk.Tk):
    #! class docstring

    def __init__(self):
        super().__init__()
        self.title('Button Sequencer')
        
        #configure window
        self.grid_columnconfigure(0,w=1) #! one space after comma between arguments
        self.grid_rowconfigure(0,w=1)
        frame = tk.Frame(self) #! frame is not really needed here, as there is only one frame you are just filling self with another single frame
        frame.grid(row=0, column=0, sticky='news') #! correct syntax between arguments
        frame.grid_columnconfigure(0,w=1)
        frame.grid_columnconfigure(1,w=1)
        frame.grid_rowconfigure(1,w=1)
        frame.grid_rowconfigure(0,w=1)
        frame.grid_rowconfigure(2,w=1)

        #add buttons, label, and entry box and bind to the respective methods
        self.Record = ttk.Button(frame, text='Record', command=self.record, state=NORMAL) #! state=NORMAL is default, you can also use strings 'normal', 'disabled' for these rather than the variables
        self.Record.grid(row=1, column=0, sticky='ew')
        self.Stop = ttk.Button(frame, text='Stop', command=self.stop, state=DISABLED)
        self.Stop.grid(row=1, column=1, sticky='ew')
        self.Play = ttk.Button(frame, text='Play', command=self.play)
        self.Play.grid(row=2,column=0,sticky='ew')
        self.inputLabel = tk.Label(frame, text='Input file name:')
        self.inputLabel.grid(row=0, column=0,sticky='e')
        self.entry = tk.Entry(frame)
        self.entry.grid(row=0, column=1, sticky='ew')
        self.Done = ttk.Button(frame, text='Done', command=self.done)
        self.Done.grid(row=2, column=1, sticky='ew')

    #done button binding
    def done(self):
        self.entry.delete(0,END) #! probably could just use a lambda function here command=lambda : self.entry.delete(0,END)

    #record button binding. Records the locations of a series of clicks to a file.
    def record(self):
        filename = self.entry.get() + '.csv'

        #check for duplicates
        if filename in os.listdir(): 
            #if a duplicate is found, ask the user if they would like to replace it
            replace = messagebox.askyesno(title="Replace saved file?", message='The filename you have input already exists. Do you want to replace it?')
            if replace:
                global recording #! should not use globals in a class use class attributes self.recording = True
                recording = True #begin recording
                self.Stop['state'] = NORMAL #make the "Stop" button not grey
        else:
            recording = True #begin recording
            self.Stop['state'] = NORMAL #make the "Stop" button not grey

    #! It is always best to avoid duplicating code like recording=True self.stop['State' ... 
    #! Something like
    #! if filename in os.listdir():
    #!     replace = ...
    #!     if not replace:
    #!           return
    #! self.recording =True
    #! self.Stop['state'] = 'normal' 
    
    #stop button binding. Ends recording
    def stop(self):
        filename = self.entry.get() + '.csv'
        global clicks, recording # again no globals
        try:
            if recording == True:  #! Never need == True an if statement is always comparing to True
                write_clicks(clicks, filename) #write click recording to a file
                print('success') #!  a print staement is not particularly helpful in a GUI, use messagebox or make a Label
            clicks = [] #clear list that temporarily stores clicks
        except: #! best not to use blanket try except, specify the error that way to catch unknown errors
            messagebox.showerror(title='Error', message='Recording was not saved. Make sure that the .csv file is not open.') #! you probably want to return after this so that the user can close the file and try againg. If you don't you will disable the stop button on them
        recording = False #turn off click recording 
        self.Stop['state'] = DISABLED #grey out stop button
    #! Comments should have at least one space after the #
    #play button binding. Plays back recording with the filename indicated in the Entry box
    def play(self):
        try:
            clicklist = pd.read_csv(self.entry.get() + '.csv', names=['x','y', 'button']) #read clicks from file into a dataframe
            #iterate through the rows of the dataframe to extract click locations
            for index, row in clicklist.iterrows():
                #left or right click based on input
                if row['button'] == 'Button.left':
                    pyautogui.click(row['x'], row['y'])
                elif row['button'] == 'Button.right':
                    pyautogui.rightClick(row['x'], row['y'])
        except: #! again don't use blanket try except
            messagebox.showerror("Error","Please input a valid filename! (.csv file extension automatically added)")

#write clicks to a .csv file
def write_clicks(clickArray, filename): #! why is this not part of the class?
    # print('writing,', clickArray[1:-2]) #! git rid of this is not using it
    with open(str(filename),'w') as clickList: #! why do you need to recast filename as a string?
        #selects a subset of clicks that excludes the first and last two clicks in the series
        for click in clickArray[1:-2]: #! not intuitive why you need to itearate over 1:-2, why does a user not want the first or last two? maybe you should start the listener after clicking record
            clickList.write(f'{click[0]},{click[1]},{click[2]}\n')

def on_click(x, y, button, pressed):
    if pressed and recording:
        clicks.append((x,y, button))
        print(x,',',y, ',',button) #! print statement not use in GUI maybe make a updating Text Box

if __name__ == '__main__':
    #start listening for clicks
    mouse_listener = mouse.Listener(on_click=on_click) #! why not in the main class? 
    mouse_listener.start()
    root = exporterGUI() 
    root.mainloop()
