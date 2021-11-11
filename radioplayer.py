import PIL
import os
import sys
import subprocess
import signal
#import requests
from PIL import Image        # sudo pip3 install pillow
from PIL import ImageTk      # sudo apt-get install python3-pil python3-pil.imagetk
import tkinter               # sudo apt-get install python3-tk
from tkinter import *
from tkinter import Tk, RIGHT, LEFT, SOLID
from tkinter import Frame, Label, Button, messagebox
import vlc                   # sudo pip3 install python-vlc


error_msg1 = "Something wrong with the formatting of radiolist.txt file. Maybe a comma is missing"
error_msg2 = "radiolist.txt non found!"
error_msg3 = "Check radiolist.txt. Internet radio address not found or not valid address for  "
error_msg4 = "NO Internet Connection!"
class App(tkinter.Tk):
    def __init__(self):
        # Depending on distro (i.e. Deepin), full path of static files may be required. That' s what next two lines are for.
        # You can put the directory with this app wherever you want in your disk
        # In elementary os and so in ubuntu comment the follwing
        pathname = os.path.dirname(sys.argv[0])
        os.chdir(pathname)
        error_flag = 0
        
        try:
            self.create_name_list()
        except IndexError:
            error_flag = 1
        except IOError:
            error_flag = 2
        tkinter.Tk.__init__(self)
        self.configure(background="#8db4c4")
        self.title("Simple Internet Radio Player")
        self.geometry("500x300+300+300")
        if error_flag == 1:
            self.display_error_message(error_msg1,1)
        if error_flag == 2:
            self.display_error_message(error_msg2,1)
        self.i = 0
        self.label_text = StringVar()  
        self.label_text.set(self.a[self.i]) 

        label = Label(self, textvariable=self.label_text, borderwidth=0, relief=SOLID, pady = 5, padx=10, foreground="#71D8F7", background="#18191E", width=32, height=2, font=("Arial",20), anchor="nw")
        label.pack(pady=15, padx=10)
        self.imgnext = ImageTk.PhotoImage(file="nxt.png",master=self)
        self.imgprev = ImageTk.PhotoImage(file="nxta.png",master=self)
        nextButton = Button(self, image=self.imgnext, width=145, height=145, borderwidth=0, highlightbackground="#100E13")
        nextButton.bind("<Button-1>",self.next_ch)
        nextButton.pack(side=RIGHT, padx=15, pady=10)
        prevButton = Button(self, image=self.imgprev, width=145, height=145, borderwidth=0, highlightbackground="#100E13")   
        prevButton.bind("<Button-1>",self.prev_ch)
        prevButton.pack(side=LEFT, padx=15, pady=10)
        
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        print([self.a[self.i]])       # Test
        self.play(self.radio[self.a[self.i]])   # First playback at program startup
## End of _init_

    # Error messages handling
    def display_error_message(self,msg,flag):          
        messagebox.showerror("Error", msg)
        if flag == 1:
            self.destroy() 
    
    # Creations of list with web radio names and addresses
    def create_name_list(self):
            self.i=0
            self.radio = {}
            # Let's open text file with web radio list
            radiolist = "radiolist.txt"
            fw = open(radiolist, "r")
            # Let' s read text file line by line
            record = fw.readline()
            while len(record) > 0:
                record_ok = record.rstrip('\n')
                splittedrecord = record_ok.split(",")
                self.radio[splittedrecord[0]] = splittedrecord[1]
                record = fw.readline()
            fw.close()
            self.a = [] 
            for name in enumerate(sorted(self.radio.keys())): # enumerate return tuple 
            # name[1] is web radio name   name[0] is record number.
            # Record number is not needed in this app as it is now. Maybe useful for future development.
            # Let's create a list with radio names
                self.a.append(name[1])      
                
    # Handler for player's buttons
    def next_ch(self, event):
        self.i += 1
        if self.i == len(self.a):
            self.i = 0
        self.label_text.set(self.a[self.i])
        self.player.stop()
        self.play(self.radio[self.a[self.i]])
    def prev_ch(self, event):
        self.i -= 1
        if self.i < 0:
            self.i = len(self.a)-1
        self.label_text.set(self.a[self.i]) 
        self.player.stop()
        self.play(self.radio[self.a[self.i]])

    # Playback the selectded radio
    def play(self,url):
        self.player = vlc.MediaPlayer(url)
        self.player.play()
        
    # When you click to exit, this function is called 
    def on_exit(self):
        self.player.stop()
        self.destroy()
        
if __name__ == '__main__':
    App().mainloop()



