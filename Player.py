import os
from tkinter import *
from tkinter import Tk
from tkinter import filedialog
from pygame import mixer


class Player:
    def __init__(self):
        self.paused = False
        root = Tk()
        root.title("Museic")
        root.geometry("920x600+290+85")
        root.configure(background='#76b5c5')
        root.resizable(True, True)
        mixer.init()

        self.Image_Icon = PhotoImage(file='img/logos/logo.png')
        self.Top = PhotoImage(file='img/background/background.png')
        self.Button_Play = PhotoImage(file='img/buttons/play.png')
        self.Button_Stop = PhotoImage(file='img/buttons/stop.png')
        self.Button_Pause = PhotoImage(file='img/buttons/pause.png')
        self.Menu = PhotoImage(file='img/logos/logo.png')
        self.Button_Folder = PhotoImage(file='img/buttons/folder.png')
        self.Button_Next = PhotoImage(file='img/buttons/next.png')
        self.Button_Previous = PhotoImage(file='img/buttons/previous.png')

        root.iconphoto(False, self.Image_Icon)
        Label(root, image=self.Top, bg='#2596be').pack()

        Button(root, image=self.Button_Play, bg='black', activebackground='black', bd=0,
               command=self.play_music).place(x=537, y=250)
        Button(root, image=self.Button_Stop, bg='black', activebackground='black', bd=0,
               command=mixer.music.stop).place(x=747, y=250)
        Button(root, image=self.Button_Pause, bg='black', activebackground='black', bd=0,
               command=self.control_pause).place(x=687, y=250)
        Button(root, image=self.Button_Next,
               bg='black', activebackground='black', bd=0).place(x=807, y=250)
        Button(root, image=self.Button_Previous,
               bg='black', activebackground='black', bd=0).place(x=627, y=250)

        Button(root, image=self.Button_Folder, bg='black', activebackground='black', bd=0,
               command=self.add_music).place(x=300, y=250)

        Label(root, image=self.Menu, bg='black').pack(
            padx=10, pady=50, side=RIGHT)
        self.Frame_Music = Frame(root, bd=2, relief=RIDGE)
        self.Frame_Music.place(x=300, y=300, width=560, height=250)

        self.Scroll = Scrollbar(self.Frame_Music)
        self.Playlist = Listbox(self.Frame_Music, width=100, font=('courier', 10), bg='#004aad',
                                fg='white', selectbackground='#5de0e6', cursor='hand2', bd=0, yscrollcommand=self.Scroll.set)
        self.Scroll.config(command=self.Playlist.yview)
        self.Scroll.pack(side=RIGHT, fill=Y)
        self.Playlist.pack(side=LEFT, fill=BOTH)

        root.mainloop()

    def add_music(self):
        path = filedialog.askdirectory()
        if path:
            os.chdir(path)
            songs = os.listdir(path)
            for song in songs:
                if song.endswith('.mp3'):
                    self.Playlist.insert(END, song)

    def play_music(self):
        mixer.music.load(self.Playlist.get(ACTIVE))
        mixer.music.play()

    def control_pause(self):
        if self.paused:
            mixer.music.unpause()
        else:
            mixer.music.pause()
        self.paused = not self.paused
