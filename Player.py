import os
from tkinter import *
from tkinter import Tk
from tkinter import filedialog
from pygame import mixer


class Player:
    def __init__(self):
        root = Tk()
        root.title("Music player")
        root.geometry("920x600+290+85")
        root.configure(background='#76b5c5')
        root.resizable(True, True)
        mixer.init()

        self.Image_Icon = PhotoImage(file='img/logos/logo.png')
        self.Top = PhotoImage(file='img/background/top.png')
        self.Logo = PhotoImage(file='img/logos/logo.png')
        self.Button_Play = PhotoImage(file='img/buttons/play.png')
        self.Button_Stop = PhotoImage(file='img/buttons/stop.png')
        self.Button_Resume = PhotoImage(file='img/buttons/resume.png')
        self.Button_Pause = PhotoImage(file='img/buttons/pause.png')
        self.Menu = PhotoImage(file='img/logos/logo.png')

        root.iconphoto(False, self.Image_Icon)
        Label(root, image=self.Top, bg='#2596be')
        Label(root, image=self.Logo, bg='white', bd=0).place(x=70, y=115)

        Button(root, image=self.Button_Play, bg='white', bd=0,
               command=self.play_music).place(x=100, y=400)
        Button(root, image=self.Button_Stop, bg='white', bd=0,
               command=mixer.music.stop).place(x=30, y=500)
        Button(root, image=self.Button_Resume, bg='white', bd=0,
               command=mixer.music.unpause).place(x=115, y=500)
        Button(root, image=self.Button_Pause, bg='white', bd=0,
               command=mixer.music.pause).place(x=200, y=500)

        Label(root, image=self.Menu, bg='white').pack(
            padx=10, pady=50, side=RIGHT)
        self.Frame_Music = Frame(root, bd=2, relief=RIDGE)
        self.Frame_Music.place(x=330, y=350, width=560, height=250)

        Button(root, text='open folder', width=15, height=2, font=('times new roman', 10,
               'bold'), fg='black', bg='white', command=self.add_music).place(x=330, y=300)

        self.Scroll = Scrollbar(self.Frame_Music)
        self.Playlist = Listbox(self.Frame_Music, width=100, font=('times new roman', 10), bg='white',
                                fg='grey', selectbackground='lightblue', cursor='hand2', bd=0, yscrollcommand=self.Scroll.set)
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
        music_name = self.Playlist.get(ACTIVE)
        mixer.music.load(self.Playlist.get(ACTIVE))
        mixer.music.play()
