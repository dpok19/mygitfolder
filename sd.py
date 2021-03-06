###############################
#names : Luke,Denish,Wyatt
#assignment: Final Project
#date 11/10/21
################################

####notes
#file only runs of python 3.8
# you have to be connected to internet to excevute file


################################
#imported Libaries and classes#
import PIL
import os
import sys
import subprocess

from PIL import Image        
from PIL import ImageTk

import tkinter               
from tkinter import *
import vlc                   
import os
import pickle
import tkinter as tk
from pygame import *
from tkinter import *
import tkinter.filedialog as filedialog
import subprocess



#Main Class
class MusicPlayer(tk.Frame):
   global frame
   frame=0
   #initilizer
   def __init__(self, master=None):
      super().__init__(master)
      self.master = master
      mixer.init()
      
      #finds the file from computer/pi folder
      ##uses picle class had to lookup how to implemtnt and use it
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
      #creates the Welcome Screen
           self.display = Label(self, text="Welcome To Rasberry PI JukeBox", anchor=E,bg="white", height=1, font=("times new roman", 45))
           self.display.grid(row=0, column=0, columnspan=4,sticky=N+E+S+W)

           self.button1=Button(self,text="listen to music",bg="blue",height="3",width="30",command=lambda:[self.clear(),self.listenmusic()])
           self.button1.grid(row=2, column=2, sticky="NSEW",columnspan=1)
           #calling the other file dinsnt execute properly, had to lookup for alternatives and used subprocessm ot call other file
           self.button2=Button(self,text="listen to Radio",bg="green",height="3",width="30",command=lambda:[subprocess.call("radioplayer.py", shell=True)])
           self.button2.grid(row=4, column=2, sticky="NSEW")

           self.homebutton=Button(self,text="Home",bg="red",command=lambda:[self.homebuttonfunction(),self.setupGUI(),self.quit_song()])
           self.homebutton.grid(row=4, column=1,)

           self.pack()

           
   def clear(self):
      #clears out the welcome page whenever the home button pressed
      self.display.grid_forget()
      self.button1.grid_forget()
      self.button2.grid_forget()

      
   def listenmusic(self):
      #the jukebox screen
      frame=2
      self.create_frames()
      self.track_widgets()
      self.control_widgets()
      self.tracklist_widgets()
      self.master.bind('<Left>', self.prev_song)
      self.master.bind('<space>', self.play_pause_song)
      self.master.bind('<Right>', self.next_song)
   
   def homebuttonfunction(self):
      #function of the home button which kills current event and goes back home page
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
      #creates all of the widgests and items for the  JukeBOX
      self.track = tk.LabelFrame(self, text='Current Song', font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=tk.GROOVE)
      self.track.config(width=410,height=300)
      self.track.grid(row=0, column=0, padx=10)

      self.tracklist = tk.LabelFrame(self, text=f'PlayList - {str(len(self.playlist))}',font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=tk.GROOVE)
      self.tracklist.config(width=190,height=375)
      self.tracklist.grid(row=0, column=1, rowspan=3, pady=5)

      self.controls = tk.LabelFrame(self,font=("times new roman",15,"bold"),bg="white",fg="white",bd=2,relief=tk.GROOVE)
      self.controls.config(width=410,height=80)
      self.controls.grid(row=2, column=0, pady=5, padx=10)


   def track_widgets(self):
      #keeps up with the songs and playslists
      self.canvas = tk.Label(self.track, image=img)
      self.canvas.configure(width=400, height=240)
      self.canvas.grid(row=0,column=0)
      
      self.songtrack = tk.Label(self.track, font=("times new roman",16,"bold"),bg="white",fg="dark blue")
      self.songtrack['text'] = 'JukeBox Music'
      self.songtrack.config(width=30, height=1)
      self.songtrack.grid(row=1,column=0,padx=10)

   def control_widgets(self):
      #controls of the buttons on bottom bar
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
      #displays all of current songs
      self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
      self.scrollbar.grid(row=0,column=1, rowspan=5, sticky='ns')

      self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE,yscrollcommand=self.scrollbar.set, selectbackground='sky blue')
      self.enumerate_songs()
      self.list.config(height=22)
      self.list.bind('<Double-1>', self.play_song) 

      self.scrollbar.config(command=self.list.yview)
      self.list.grid(row=0, column=0, rowspan=5)

   def retrieve_songs(self):
      #adds song into the playlist
      self.songlist = []
      directory = filedialog.askdirectory()
      #use of os and systrem libarries to handle importing files from computer folder
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
      #adds song into the playlist
      for index, song in enumerate(self.playlist):
         self.list.insert(index, os.path.basename(song))

   def play_pause_song(self, event):
      # plays and stops button functions
      if self.paused:
         self.play_song()
      else:
         self.pause_song()

   def play_song(self, event=None):
      # play current selected song
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
      #stop sound
       mixer.music.pause()
   
   def pause_song(self):
      #pause the song and move on to next one
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
      #fucntion for the prevouis button
      self.master.focus_set()
      if self.current > 0:
         self.current -= 1
      else:
         self.current = 0
      self.list.itemconfigure(self.current + 1, bg='white')
      self.play_song()


   def next_song(self, event=None):
      #fucntion for the next button
      self.master.focus_set()
      if self.current < len(self.playlist) - 1:
         self.current += 1
      else:
         self.current = 0
      self.list.itemconfigure(self.current - 1, bg='white')
      self.play_song()


   def change_volume(self, event=None):
      #change the volumes 
      self.v = self.volume.get()
      mixer.music.set_volume(self.v / 10)
      pass


        

        

#Creating the Tkinter Window
root = tk.Tk()
root.attributes('-fullscreen',False)
root.title('Rasberry Pi Jukebox')

#image files
img = PhotoImage(file='jukebox.gif')
next_ = PhotoImage(file = 'next.gif')
prev = PhotoImage(file='previous.gif')
play = PhotoImage(file='play.gif')
pause = PhotoImage(file='pause.gif')
home=PhotoImage(file='home.gif')

app = MusicPlayer(master=root)
app.mainloop()







