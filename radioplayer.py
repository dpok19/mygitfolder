#rasberry Pi jukebox
#Radio Player file that is called in the main program


import os
from PIL import *      # sudo pip3 install pillow
from PIL import ImageTk      # sudo apt-get install python3-pil python3-pil.imagetk
import tkinter               # sudo apt-get install python3-tk
from tkinter import *
import vlc                   # sudo pip3 install python-vlc

class App(tkinter.Tk):
    def __init__(self):
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
        print([self.a[self.i]])       
        self.play(self.radio[self.a[self.i]])   


    
    
    
    # Creations of list with web radio names and addresses
    def create_name_list(self):
            self.i=0
            self.radio = {}
            #file with the urls for radio sations
            radiolist = "radiolist.txt"
            fw = open(radiolist, "r")
            record = fw.readline()
            while len(record) > 0:
                record_ok = record.rstrip('\n')
                splittedrecord = record_ok.split(",")
                self.radio[splittedrecord[0]] = splittedrecord[1]
                record = fw.readline()
            fw.close()
            self.a = [] 
            for name in enumerate(sorted(self.radio.keys())):
                #creates list of stations and break up name and urls
                self.a.append(name[1])      
                
    #next button function
    def next_ch(self, event):
        self.i += 1
        if self.i == len(self.a):
            self.i = 0
        self.label_text.set(self.a[self.i])
        self.player.stop()
        self.play(self.radio[self.a[self.i]])


    #prevois button function
    def prev_ch(self, event):
        self.i -= 1
        if self.i < 0:
            self.i = len(self.a)-1
        self.label_text.set(self.a[self.i]) 
        self.player.stop()
        self.play(self.radio[self.a[self.i]])
        

    # Play the selectded radio
    def play(self,url):
        self.player = vlc.MediaPlayer(url)
        self.player.play()
        
    #closing out of the 
    def on_exit(self):
        self.player.stop()
        self.destroy()
        
App().mainloop()



