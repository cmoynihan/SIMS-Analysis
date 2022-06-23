from ast import Delete
import tkinter as tk 
import os
from tkinter import DISABLED, END, NORMAL, ttk, messagebox
import pyautogui
import pandas as pd
from pynput import mouse


#GUI window class
class recorderGUI(tk.Tk):
    '''
    GUI class for click recorder. Has 6 buttons: Record, Pause, Stop, Play, Done, Add Text Marker, and an entry box.
    Record: Records a sequence of clicks until the user clicks Stop. Can record left and right clicks
    Pause: Pauses the recording until user clicks Record again
    Stop: Stops the recording and writes to a .csv with the name indicated in the entry box
    Play: Reads the .csv file with the name in the entry box, then reproduces the clicks with pyautogui
    Clear: Clears the entry box
    Add Text Marker: Adds an entry to the .csv file indicating to the reader program that text goes here
    
    
    '''
    
    def __init__(self):
        super().__init__()
        self.title('Button Sequencer')
        self.recording = False
        self.clicks = []
        self.paused = False
        self.attributes('-topmost', True)
        mouse_listener = mouse.Listener(on_click=self.on_click)
        mouse_listener.start()

        pyautogui.PAUSE = 1 # delay (in seconds) between pyautogui calls        
        
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
        frame.grid_rowconfigure(3, w=1)
        frame.grid_rowconfigure(4, w=1)

        #add buttons, label, and entry box and bind to the respective methods
        self.Record = ttk.Button(frame, text='Record', command=self.record, state=NORMAL) 
        self.Record.grid(row=1, column=0, sticky='ew')
        self.Stop = ttk.Button(frame, text='Stop', command=self.stop, state=DISABLED)
        self.Stop.grid(row=1, column=1, sticky='ew')
        self.Play = ttk.Button(frame, text='Play', command=self.play)
        self.Play.grid(row=2, column=1, sticky='ew')
        self.Pause = ttk.Button(frame, text='Pause', command=self.pause, state=DISABLED)
        self.Pause.grid(row=2, column=0, sticky='ew')
        self.inputLabel = tk.Label(frame, text='Input file name:')
        self.inputLabel.grid(row=0, column=0, sticky='e')
        self.entry = tk.Entry(frame)
        self.entry.grid(row=0, column=1, sticky='ew')
        self.Clear = ttk.Button(frame, text='Clear', command=self.clear)
        self.Clear.grid(row=3, column=0, sticky='ew')
        self.AddTextMarker = ttk.Button(frame, text='Add Text Marker', command=self.addTextMarker, state=DISABLED)
        self.AddTextMarker.grid(row=3, column=1, sticky='ew')
        self.Loop = ttk.Button(frame, text='Begin Loop', command=self.toggleLoop, state=DISABLED)
        self.Loop.grid(row=4, column=0, sticky='ew')
        self.Del = ttk.Button(frame, text='Delete Last Click', command=self.delete, state=DISABLED)
        self.Del.grid(row=4, column=1, sticky='ew')

        # disable window resizing
        self.resizable(False, False)

    # clear button binding
    def clear(self):
        self.entry.delete(0,END)

    # record button binding. Records the locations of a series of clicks to a file.
    def record(self):
        if not self.paused:
            # Check for invalid characters
            banned = '/\.?%'
            if any(elem in self.entry.get() for elem in banned) or len(self.entry.get()) == 0:
                messagebox.showerror(title='Error', message='Please input a valid filename!')
                self.clear()
                return
            filename = self.entry.get() + '.csv'
            # check for duplicates
            if filename in os.listdir('clickSequences'):
                #if a duplicate is found, ask the user if they would like to replace it
                replace = messagebox.askyesno(title="Replace saved file?", message='The filename you have input already exists. Do you want to replace it?')
                if not replace:
                    return
            self.entry['state'] = DISABLED
            self.Play['state'] = DISABLED
            self.Clear['state'] = DISABLED
        self.AddTextMarker['state'] = NORMAL
        self.Record['state'] = DISABLED
        self.Pause['state'] = NORMAL
        self.Loop['state'] = NORMAL
        self.Del['state'] = NORMAL
        self.paused = False
        self.recording = True
        self.Stop['state'] = NORMAL #make the "Stop" button not grey
        
    #stop button binding. Ends recording
    def stop(self):
        try:
            filename = self.entry.get() + '.csv'
            if self.Loop['text'] == 'End Loop':
                self.toggleLoop()
                self.write_clicks(filename, clip=False) # write click recording to a file without clipping
            else:
                self.write_clicks(filename)
            messagebox.showinfo(message='Recording saved!')
        except PermissionError:
            self.pause() # pause so that recorder doesn't record the user closing out
            ok = messagebox.askokcancel(title='Permission Error', message='Recording cannot be saved. Close the .csv file if it is open and click OK.') 
            if ok:
                self.stop()
        self.recording = False # turn off click recording 
        self.paused = False
        self.Pause['state'] = DISABLED
        self.Stop['state'] = DISABLED # grey out stop button
        self.Record['state'] = NORMAL
        self.entry['state'] = NORMAL
        self.Del['state'] = DISABLED
        self.Play['state'] = NORMAL
        self.Clear['state'] = NORMAL
        self.AddTextMarker['state'] = DISABLED
        self.Loop['state'] = DISABLED
        self.clicks = []

    # pause button method
    def pause(self):
        if self.recording:
            self.paused = True
            self.recording = False
            self.clicks.pop()
            self.Record['state'] = NORMAL
            self.AddTextMarker['state'] = DISABLED
            self.Pause['state'] = DISABLED

    # play button binding. Plays back recording with the filename indicated in the Entry box
    def play(self):
        try:
            clicklist = pd.read_csv(os.path.join('clickSequences', self.entry.get() + '.csv'), names=['x','y', 'button']) # read clicks from file into a dataframe
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="File not found")
            self.clear()
            return

        self.withdraw() # hide the window
        # iterate through the rows of the dataframe to extract click locations
        for index, row in clicklist.iterrows():
            if row['x'] != 'Text':
                # left or right click based on input
                pos = tuple((row['x'], row['y']))
                if row['button'] == 'Button.left':
                    pyautogui.click(pos)
                elif row['button'] == 'Button.right':
                    pyautogui.rightClick(pos)
        self.deiconify() # show the window
    
    def addTextMarker(self):
        self.clicks[-1] = ('Text','Text','Text') # replace the click on this button with a marker for the csv reader to parse

    def toggleLoop(self):
        if self.Loop['text'] == 'Begin Loop':
            self.Loop['text'] = 'End Loop'
        else:
            self.Loop['text'] = 'Begin Loop'
        self.clicks[-1] = ('Loop', 'Loop', 'Loop')
    
    def delete(self):
        self.clicks.pop()
        self.clicks.pop()

    # write clicks to a .csv file
    def write_clicks(self, filename, clip=True):
        if 'clickSequences' not in os.listdir():
            os.mkdir('clickSequences')
        with open(os.path.join('.', 'clickSequences', filename),'w') as clickList: 
            if clip:
                for click in self.clicks[0:-1]: # clip out last click
                    clickList.write(f'{click[0]},{click[1]},{click[2]}\n')
            else:
                for click in self.clicks:
                    clickList.write(f'{click[0]},{click[1]},{click[2]}\n')

    # method to add clicks to list
    def on_click(self, x, y, button, pressed):
        if pressed and self.recording:
            self.clicks.append((x,y, button))

if __name__ == '__main__':
    root = recorderGUI() 
    root.mainloop()