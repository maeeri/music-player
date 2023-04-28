import os
from tkinter import *
from tkinter import Tk
from tkinter import filedialog
from pygame import mixer
import json


class Player:
    def __init__(self):
        self.paused = False
        self.btns_filepath = 'txt/btns.json'
        self.preferences_filepath = 'txt/preferences.json'
        self.preferences = {}
        self.songs = []
        self.curr_song = 0

        with open(self.preferences_filepath) as pref_file:
            content = json.load(pref_file)
            if content:
                self.preferences = content

    def loop(self):
        root = Tk()
        root.title("Museic")
        root.geometry("920x600+290+85")
        root.configure(background='#76b5c5')
        root.resizable(False, False)
        mixer.init()

        self.Background = PhotoImage(file='img/background.png')
        Label(root, image=self.Background, bg='#2596be').pack()

        self.draw_buttons(root)

        self.draw_playlist(root)

        if self.preferences['path']:
            self.get_music(self.preferences['path'])

        root.mainloop()

    def get_music(self, path):
        os.chdir(path)
        self.songs = os.listdir(path)
        for song in self.songs:
            if song.endswith('.mp3'):
                self.Area_Playlist.insert(END, song)
        self.queue_music()

    def add_music(self):
        path = filedialog.askdirectory()
        if path:
            if not self.preferences["path"] or path != self.preferences["path"]:
                self.preferences["path"] = path
                json_object = json.dumps(self.preferences)
                print(json_object)
                with open(self.preferences_filepath, 'w') as pref_file:
                    pref_file.write(json_object)
            os.chdir(path)
            songs = os.listdir(path)
            for song in songs:
                if song.endswith('.mp3'):
                    self.Area_Playlist.insert(END, song)

    def play_music(self):
        self.curr_song = self.Area_Playlist.curselection()[0] if self.Area_Playlist.curselection() else self.curr_song
        mixer.music.load(self.Area_Playlist.get(ACTIVE))
        mixer.music.play()

    def control_pause(self):
        if self.paused:
            mixer.music.unpause()
        else:
            mixer.music.pause()
        self.paused = not self.paused

    def draw_buttons(self, root):
        self.Button_Play = PhotoImage(
            file='img/buttons/play.png')
        Button(root, image=self.Button_Play, bg='black', activebackground='black', bd=0,
               command=self.play_music).place(x=537, y=250)

        self.Button_Stop = PhotoImage(file='img/buttons/stop.png')
        Button(root, image=self.Button_Stop, bg='black', activebackground='black', bd=0,
               command=mixer.music.stop).place(x=747, y=250)

        self.Button_Previous = PhotoImage(file='img/buttons/previous.png')
        Button(root, image=self.Button_Previous,
               bg='black', activebackground='black', command=self.prev_song, bd=0).place(x=627, y=250)

        self.Button_Pause = PhotoImage(file='img/buttons/pause.png')
        Button(root, image=self.Button_Pause, bg='black', activebackground='black', bd=0,
               command=self.control_pause).place(x=687, y=250)

        self.Button_Folder = PhotoImage(file='img/buttons/folder.png')
        Button(root, image=self.Button_Folder, bg='black', activebackground='black', bd=0,
               command=self.add_music).place(x=300, y=250)

        self.Button_Next = PhotoImage(file='img/buttons/next.png')
        Button(root, image=self.Button_Next,
               bg='black', activebackground='black', command=self.next_song, bd=0).place(x=807, y=250)

    def draw_playlist(self, root):
        self.Frame_Music = Frame(root, bd=2, relief=RAISED)
        self.Frame_Music.place(x=300, y=300, width=560, height=250)

        self.Scroll = Scrollbar(self.Frame_Music, width=13, bg='white',
                                activebackground='grey', highlightcolor='yellow')
        self.Area_Playlist = Listbox(self.Frame_Music, width=100, font=('courier new', 10), bg='#004aad',
                                     fg='white', selectbackground='#5de0e6', cursor='hand2', bd=0, yscrollcommand=self.Scroll.set)
        self.Scroll.config(command=self.Area_Playlist.yview)
        self.Scroll.pack(side=RIGHT, fill=Y)
        self.Area_Playlist.pack(side=LEFT, fill=BOTH)

    def next_song(self):
        self.curr_song += 1
        self.Area_Playlist.activate(self.curr_song)
        self.play_music()

    def prev_song(self):
        if mixer.music.get_pos() > 5100:
            print(mixer.music.get_pos())
            mixer.music.set_pos(0)
        else:
            self.curr_song -= 1
            self.Area_Playlist.activate(self.curr_song)
            self.play_music()

    def queue_music(self):
        for song in self.songs:
            if song.endswith('.mp3'):
                mixer.music.queue(song)
