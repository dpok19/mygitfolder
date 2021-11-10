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
import radioplayer
import os
import pickle
import tkinter as tk
from pygame import *
from tkinter import *
import tkinter.filedialog as filedialog


#class Welcome(tk.frame):
#        def __init__(self, master=None):
#                super().__init__(master)
#  def main_account_screen(self):
#                main_screen.geometry("300x250") # set the configuration of GUI window
#                main_screen.title("Pi Music") # set the title of GUI window
# 
#        # create a Form label
#                Label(text="Welcome to Pi Music", bg="white", width="300", height="2", font=("Calibri", 13)).pack() 
#                Label(text="Choose an option below").pack() 
# 
        # create Login Button 
#                Button(text="Listen To Music", height="2", width="30").pack() 

 
        # create a register button
 #                Button(text="Listen To Radio", height="2", width="30").pack()
 #                main_screen.mainloop()
 


class MusicPlayer(tk.Frame):
   global frame
   frame=0
   def __init__(self, master=None):
      super().__init__(master)
      self.master = master
      mixer.init()

      if os.path.exists('songs.pickle'):
         with open('songs.pickle', 'rb') as f:
            self.playlist = pickle.load(f)
      else:
                        self.playlist=[]
                
      self.current = 0
      self.paused = True
      self.played = False
      self.setupGUI()
      frame=1
      self.pack()
   def setupGUI(self):
           self.display = Label(self, text="Welcome To Music PI", anchor=E,bg="white", height=1, font=("times new roman", 45))
           self.display.grid(row=0, column=0, columnspan=4,sticky=N+E+S+W)
           self.button1=Button(self,text="listen to music",bg="blue",height="3",width="30",command=lambda:[self.clear(),self.listenmusic()])
           self.button1.grid(row=2, column=2, sticky="NSEW",columnspan=1)
           self.button2=Button(self,text="listen to Radio",bg="green",height="3",width="30",command=lambda:[App().mainloop()])
           self.button2.grid(row=4, column=2, sticky="NSEW")
           self.homebutton=Button(self,text="Home",bg="red",command=lambda:[self.homebuttonfunction(),self.setupGUI(),self.quit_song()])
           self.homebutton.grid(row=4, column=1,)
           self.pack()
   def clear(self):
      self.display.grid_forget()
      self.button1.grid_forget()
      self.button2.grid_forget()
   def listenmusic(self):
      frame=2
      self.create_frames()
      self.track_widgets()
      self.control_widgets()
      self.tracklist_widgets()

      self.master.bind('<Left>', self.prev_song)
      self.master.bind('<space>', self.play_pause_song)
      self.master.bind('<Right>', self.next_song)
   
   def homebuttonfunction(self):
      self.track.grid_forget()
      self.tracklist.grid_forget()
      self.controls.grid_forget()
      self.canvas.grid_forget()
      self.songtrack.grid_forget()
      self.loadSongs.grid_forget()
      self.prev.grid_forget()
      self.next.grid_forget()
      self.pause.grid_forget()
      self.slider.grid_forget()
      self.list.grid_forget()

   
      
      
        
   def create_frames(self):
      self.track = tk.LabelFrame(self, text='Current Song', font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=tk.GROOVE)
      self.track.config(width=410,height=300)
      self.track.grid(row=0, column=0, padx=10)

      self.tracklist = tk.LabelFrame(self, text=f'PlayList - {str(len(self.playlist))}',
                     font=("times new roman",15,"bold"),
                     bg="grey",fg="white",bd=5,relief=tk.GROOVE)
      self.tracklist.config(width=190,height=375)
      self.tracklist.grid(row=0, column=1, rowspan=3, pady=5)

      self.controls = tk.LabelFrame(self,
                     font=("times new roman",15,"bold"),
                     bg="white",fg="white",bd=2,relief=tk.GROOVE)
      self.controls.config(width=410,height=80)
      self.controls.grid(row=2, column=0, pady=5, padx=10)

   def track_widgets(self):
      self.canvas = tk.Label(self.track, image=img)
      self.canvas.configure(width=400, height=240)
      self.canvas.grid(row=0,column=0)

      self.songtrack = tk.Label(self.track, font=("times new roman",16,"bold"),
                  bg="white",fg="dark blue")
      self.songtrack['text'] = 'Pi Music'
      self.songtrack.config(width=30, height=1)
      self.songtrack.grid(row=1,column=0,padx=10)

   def control_widgets(self):
      self.loadSongs = tk.Button(self.controls, bg='red', fg='white', font=10)
      self.loadSongs['text'] = 'Load Songs'
      self.loadSongs['command'] = self.retrieve_songs
      self.loadSongs.grid(row=0, column=0, padx=10)

      self.prev = tk.Button(self.controls, image=prev)
      self.prev['command'] = self.prev_song
      self.prev.grid(row=0, column=1)

      self.pause = tk.Button(self.controls, image=pause)
      self.pause['command'] = self.pause_song
      self.pause.grid(row=0, column=2)

      self.next = tk.Button(self.controls, image=next_)
      self.next['command'] = self.next_song
      self.next.grid(row=0, column=3)

      self.volume = tk.DoubleVar(self)
      self.slider = tk.Scale(self.controls, from_ = 0, to = 10, orient = tk.HORIZONTAL)
      self.slider['variable'] = self.volume
      self.slider.set(8)
      mixer.music.set_volume(0.8)
      self.slider['command'] = self.change_volume
      self.slider.grid(row=0, column=4, padx=5)


   def tracklist_widgets(self):
      self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
      self.scrollbar.grid(row=0,column=1, rowspan=5, sticky='ns')

      self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE,
                yscrollcommand=self.scrollbar.set, selectbackground='sky blue')
      self.enumerate_songs()
      self.list.config(height=22)
      self.list.bind('<Double-1>', self.play_song) 

      self.scrollbar.config(command=self.list.yview)
      self.list.grid(row=0, column=0, rowspan=5)

   def retrieve_songs(self):
      self.songlist = []
      directory = filedialog.askdirectory()
      for root_, dirs, files in os.walk(directory):
            for file in files:
               if os.path.splitext(file)[1] == '.mp3':
                  path = (root_ + '/' + file).replace('\\','/')
                  self.songlist.append(path)

      with open('songs.pickle', 'wb') as f:
         pickle.dump(self.songlist, f)
      self.playlist = self.songlist
      self.tracklist['text'] = f'PlayList - {str(len(self.playlist))}'
      self.list.delete(0, tk.END)
      self.enumerate_songs()

   def enumerate_songs(self):
      for index, song in enumerate(self.playlist):
         self.list.insert(index, os.path.basename(song))

   def play_pause_song(self, event):
      if self.paused:
         self.play_song()
      else:
         self.pause_song()

   def play_song(self, event=None):
      if event is not None:
         self.current = self.list.curselection()[0]
         for i in range(len(self.playlist)):
            self.list.itemconfigure(i, bg="white")

      print(self.playlist[self.current])
      mixer.music.load(self.playlist[self.current])
      self.songtrack['anchor'] = 'w' 
      self.songtrack['text'] = os.path.basename(self.playlist[self.current])

      self.pause['image'] = play
      self.paused = False
      self.played = True
      self.list.activate(self.current) 
      self.list.itemconfigure(self.current, bg='sky blue')

      mixer.music.play()
   def quit_song(self):
       mixer.music.pause()

   def pause_song(self):
      if not self.paused:
         self.paused = True
         mixer.music.pause()
         self.pause['image'] = pause
      else:
         if self.played == False:
            self.play_song()
         self.paused = False
         mixer.music.unpause()
         self.pause['image'] = play

   def prev_song(self, event=None):
      self.master.focus_set()
      if self.current > 0:
         self.current -= 1
      else:
         self.current = 0
      self.list.itemconfigure(self.current + 1, bg='white')
      self.play_song()

   def next_song(self, event=None):
      self.master.focus_set()
      if self.current < len(self.playlist) - 1:
         self.current += 1
      else:
         self.current = 0
      self.list.itemconfigure(self.current - 1, bg='white')
      self.play_song()

   def change_volume(self, event=None):
      self.v = self.volume.get()
      mixer.music.set_volume(self.v / 10)
   def listenradio(self):
      frame=3
      self.play = tk.LabelFrame(self, text='Current Song', font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=tk.GROOVE)
      self.t.config(width=410,height=300)
      self.track.grid(row=0, column=0, padx=10)
      
      pass
#items=[self.track,self.tracklist,self.controls,self.canvas,self.loadSongs,self.songtrack,self.prev,self.pause,self.next,self.volume,self.slider,self.scrollbar,self.list]

# ----------------------------- Main -------------------------------------------

error_msg1 = "Something wrong with the formatting of radiolist.txt file. Maybe a comma is missing"
error_msg2 = "radiolist.txt non found!"
error_msg3 = "Check radiolist.txt. Internet radio address not found or not valid address for  "
error_msg4 = "NO Internet Connection!"
class App(tkinter.Tk):
   global current
   current=("")
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
        self.configure(background="#100E13")
        self.title("Radio Player")
        self.geometry("500x300+300+300")
        if error_flag == 1:
            self.display_error_message(error_msg1,1)
        if error_flag == 2:
            self.display_error_message(error_msg2,1)
        self.i = 0
        self.label_text = StringVar()  
        self.label_text.set(self.a[self.i])
        global current
        current=self.a[self.i]

        self.label = Label(self, textvariable=self.label_text, borderwidth=0, relief=SOLID, pady = 5, padx=10, foreground="#71D8F7", background="#18191E", width=32, height=2, font=("Arial",20), anchor="nw")
        self.label.pack(pady=15, padx=10)
        self.imgnext = ImageTk.PhotoImage(file="nextbutton.png",master=self)
        self.imgprev = ImageTk.PhotoImage(file="prevbutton.png",master=self)
        nextButton = Button(self, image=self.imgnext, width=145, height=145, borderwidth=0, highlightbackground="#100E13")
        nextButton.bind("<Button-1>",self.next_ch)
        nextButton.pack(side=RIGHT, padx=15, pady=10)
        prevButton = Button(self, image=self.imgprev, width=145, height=145, borderwidth=0, highlightbackground="#100E13")   
        prevButton.bind("<Button-1>",self.prev_ch)
        prevButton.pack(side=LEFT, padx=15, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        
        print([self.a[self.i]])       # Test
        self.play(self.radio[self.a[self.i]])   # First playback at program startup
   


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
        self.label_text=(self.a[self.i])
        global current
        current=self.a[self.i]
        self.player.stop()
        self.play(self.radio[self.a[self.i]])
   def prev_ch(self, event):
        self.i -= 1
        if self.i < 0:
            self.i = len(self.a)-1
        self.label_text=self.a[self.i]
        global current
        current=self.a[self.i]
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
       
       
    
        



root = tk.Tk()
root.geometry('700x400')
root.title('Rasberry Pi Jukebox')

img = PhotoImage(file='jukebox.gif')
next_ = PhotoImage(file = 'next.gif')
prev = PhotoImage(file='previous.gif')
play = PhotoImage(file='play.gif')
pause = PhotoImage(file='pause.gif')
home=PhotoImage(file='home.gif')

app = MusicPlayer(master=root)
app.mainloop()






