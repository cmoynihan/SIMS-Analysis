import tkinter as tk 
import os
from tkinter import DISABLED, END, NORMAL, ttk, messagebox
import pyautogui
import pandas as pd
from pynput import mouse

pyautogui.PAUSE = 1 # delay (in seconds) between pyautogui calls
recording = False # False if the program is not recording to the click list, True if it is
clicks = [] #list to temporarily store locations of clicks during recording
screenWidth, screenHeight = pyautogui.size() #! this is never used again, why is it needed?

#GUI window class
class recorderGUI(tk.Tk):
    '''
    GUI class for click recorder. Has 4 buttons: Record, Stop, Play, Done, and an entry box.

    Record: Records a sequence of clicks until the user clicks Stop. Can record left and right clicks
    Stop: Stops the recording and writes to a .csv with the name indicated in the entry box
    Play: Reads the .csv file with the name in the entry box, then reproduces the clicks with pyautogui
    Done: Clears the entry box
    '''
    
    def __init__(self):
        super().__init__()
        self.title('Button Sequencer')
        self.recording = False
        self.clicks = []
        mouse_listener = mouse.Listener(on_click=self.on_click)
        mouse_listener.start()
        
        #configure window
        self.grid_columnconfigure(0, w=1) 
        self.grid_rowconfigure(0, w=1)
        frame = tk.Frame(self)
        frame.grid(row=0, column=0, sticky='news')
        frame.grid_columnconfigure(0, w=1)
        frame.grid_columnconfigure(1, w=1)
        frame.grid_rowconfigure(1, w=1)
        frame.grid_rowconfigure(0, w=1)
        frame.grid_rowconfigure(2, w=1)

        #add buttons, label, and entry box and bind to the respective methods
        self.Record = ttk.Button(frame, text='Record', command=self.record, state=NORMAL) 
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
        banned = '/\.?%'
        if any(elem in self.entry.get() for elem in banned):
            messagebox.showerror(title='Error', message='Please input a valid filename!')
            self.done()
            return
        
        filename = self.entry.get() + '.csv'

        #check for duplicates
        if filename in os.listdir(): 
            #if a duplicate is found, ask the user if they would like to replace it
            replace = messagebox.askyesno(title="Replace saved file?", message='The filename you have input already exists. Do you want to replace it?')
            if not replace:
                return
    
        self.recording = True
        self.Stop['state'] = NORMAL #make the "Stop" button not grey
    
    #stop button binding. Ends recording
    def stop(self):
        filename = self.entry.get() + '.csv'
        self.recording = False # turn off click recording 
        self.Stop['state'] = DISABLED # grey out stop button
        # try:
        write_clicks(self.clicks, filename) #write click recording to a file
        messagebox.showinfo(message='Recording saved!')
        self.clicks = [] # clear list that temporarily stores clicks
        # except: #! best not to use blanket try except, specify the error that way to catch unknown errors
        #     messagebox.showerror(title='Error', message='Recording was not saved. Make sure that the .csv file is not open.') #! you probably want to return after this so that the user can close the file and try againg. If you don't you will disable the stop button on them
        
    # play button binding. Plays back recording with the filename indicated in the Entry box
    def play(self):
        try:
            clicklist = pd.read_csv(self.entry.get() + '.csv', names=['x','y', 'button']) # read clicks from file into a dataframe
            # iterate through the rows of the dataframe to extract click locations
            print(clicklist)
            for index, row in clicklist.iterrows():
                # left or right click based on input
                if row['button'] == 'Button.left':
                    pyautogui.click(row['x'], row['y'])
                elif row['button'] == 'Button.right':
                    pyautogui.rightClick(row['x'], row['y'])
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="File not found")
            self.done()
        
        # except: #! again don't use blanket try except
        #     messagebox.showerror("Error","Please input a valid filename! (.csv file extension automatically added)")
    
    # method to add clicks to list
    def on_click(self, x, y, button, pressed):
        if pressed and self.recording:
            self.clicks.append((x,y, button))
            print(x,',',y, ',',button) #! print statement not use in GUI maybe make a updating Text Box

# write clicks to a .csv file
def write_clicks(clickArray, filename): #! why is this not part of the class?
    # print('writing,', clickArray[1:-2]) #! git rid of this is not using it
    with open(str(filename),'w') as clickList: #! why do you need to recast filename as a string?
        #selects a subset of clicks that excludes the first and last two clicks in the series
        for click in clickArray[1:-2]: #! not intuitive why you need to itearate over 1:-2, why does a user not want the first or last two? maybe you should start the listener after clicking record
            clickList.write(f'{click[0]},{click[1]},{click[2]}\n')



if __name__ == '__main__':
    tk.DISABLED
    # start listening for clicks

    root = recorderGUI() 
    root.mainloop()
