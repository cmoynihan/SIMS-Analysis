
import tkinter as tk
from tkinter import DISABLED, END, NORMAL, ttk
from tkinter import messagebox
import clickRecorder
import pyautogui
import pandas as pd
from pynput import mouse
import os

#GUI window class
class exporterGUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Button Sequencer')
        
        #configure window
        self.grid_columnconfigure(0,w=1)
        self.grid_rowconfigure(0,w=1)
        frame = tk.Frame(self)
        frame.grid(row=0, column=0, sticky='news')
        frame.grid_columnconfigure(0,w=1)
        frame.grid_columnconfigure(1,w=1)
        frame.grid_rowconfigure(1,w=1)
        frame.grid_rowconfigure(0,w=1)
        frame.grid_rowconfigure(2,w=1)

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
        self.entry.delete(0,END)

    #record button binding. Records the locations of a series of clicks to a file.
    def record(self):
        filename = self.entry.get() + '.csv'

        #check for duplicates
        if filename in os.listdir(): 
            #if a duplicate is found, ask the user if they would like to replace it
            replace = messagebox.askyesno(title="Replace saved file?", message='The filename you have input already exists. Do you want to replace it?')
            if replace:
                clickRecorder.recording = True #begin recording
                self.Stop['state'] = NORMAL #make the "Stop" button not grey
        else:
            clickRecorder.recording = True #begin recording
            self.Stop['state'] = NORMAL #make the "Stop" button not grey
    
    #stop button binding. Ends recording
    def stop(self):
        filename = self.entry.get() + '.csv'

        try:

            if clickRecorder.recording == True:
                clickRecorder.write_clicks(clickRecorder.clicks, filename) #write click recording to a file
            clickRecorder.recording = False #turn off click recording
            clickRecorder.clicks = [] #clear list that temporarily stores clicks
        except:
            messagebox.showerror(title='Error', message='Recording was not saved. Make sure that the .csv file is not open.')
        self.Stop['state'] = DISABLED #grey out stop button
        
    #play button binding. Plays back recording with the filename indicated in the Entry box
    def play(self):
        try:
            clicks = pd.read_csv(self.entry.get() + '.csv', names=['x','y', 'button']) #read clicks from file into a dataframe
            #iterate through the rows of the dataframe to extract click locations
            for index, row in clicks.iterrows():
                #left or right click based on input
                if row['button'] == 'Button.left':
                    pyautogui.click(row['x'], row['y'])
                elif row['button'] == 'Button.right':
                    pyautogui.rightClick(row['x'], row['y'])
        except:
            messagebox.showerror("Error","Please input a valid filename! (.csv file extension automatically added)")

if __name__ == '__main__':
    #start listening for clicks
    mouse_listener = mouse.Listener(on_click=clickRecorder.on_click)
    mouse_listener.start()
    root = exporterGUI()
    root.mainloop()