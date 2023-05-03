import os
from tkinter import *
from tkinter import Tk, ttk
from tkinter import filedialog
from pygame import mixer
from pygame import *
import pygame
from mutagen import mp3
import json


class Player:
    def __init__(self):
        self.paused = False
        self.filepath_pref = 'txt/preferences.json'
        self.preferences = {}
        self.song_files = []
        self.songnames = []
        self.song = None
        self.curr_song = 0
        self.SONGEND = pygame.event.custom_type()

        with open(self.filepath_pref) as pref_file:
            content = json.load(pref_file)
            if content:
                self.preferences = content

        self.loop()

    # creates app root
    def create_root(self):
        self.root = Tk()
        self.root.title("Museic")
        self.root.geometry("920x600+290+85")
        self.root.configure(background='#76b5c5')
        self.root.resizable(False, False)

    # places all elements
    def draw_window(self):
        self.draw_background()
        self.draw_buttons()
        self.draw_playlist()

    def update(self):
        for event in pygame.event.get():
            print(event.type)
            if event.type == self.SONGEND:
                self.next_song()
        self.Playlist.after(1000, lambda: self.update())

    def loop(self):
        self.create_root()
        mixer.init()
        pygame.init()
        mixer.music.set_endevent(self.SONGEND)

        self.style = ttk.Style()
        self.style.theme_use('winnative')
        self.style.configure('black.Horizontal.TProgressbar', foreground='black', background='black')
        self.draw_window()

        if self.preferences and 'path' in self.preferences:
            self.get_music(self.preferences['path'])

        
        self.root.after(1000, self.update)
        self.root.mainloop()

    # loads latest playlist from json file
    def get_music(self, path):
        os.chdir(path)
        self.song_files = os.listdir(path)
        for song in self.song_files:
            if song.endswith('.mp3'):
                self.Playlist.insert(END, song)
                self.songnames.append(self.get_name(song))

    # opens file dialog and gets path to folder,
    def add_music(self):
        path = filedialog.askdirectory()
        if path:
            if 'path' not in self.preferences:
                self.preferences["path"] = path
                json_object = json.dumps(self.preferences)
                
                with open(self.filepath_pref, 'w') as pref_file:
                    pref_file.write(json_object)
            os.chdir(path)
            self.song_files = os.listdir(path)
            for song in self.song_files:
                if song.endswith('.mp3'):
                    self.Playlist.insert(END, song)

    # creates the buttons to control actions
    def draw_buttons(self):
        y_base = 220
        x_base = 533
        self.Button_Play = PhotoImage(
            file='img/buttons/play.png')
        Button(self.root, image=self.Button_Play, bg='black', activebackground='black', bd=0,
               command=self.play_music).place(x=x_base, y=y_base)

        self.Button_Stop = PhotoImage(file='img/buttons/stop.png')
        Button(self.root, image=self.Button_Stop, bg='black', activebackground='black', bd=0,
               command=self.stop_music).place(x=x_base+220, y=y_base)

        self.Button_Previous = PhotoImage(file='img/buttons/previous.png')
        Button(self.root, image=self.Button_Previous,
               bg='black', activebackground='black', command=self.prev_song, bd=0).place(x=x_base + 100, y=y_base)

        self.Button_Pause = PhotoImage(file='img/buttons/pause.png')
        Button(self.root, image=self.Button_Pause, bg='black', activebackground='black', bd=0,
               command=self.control_pause).place(x=x_base+160, y=y_base)

        self.Button_Folder = PhotoImage(file='img/buttons/folder.png')
        Button(self.root, image=self.Button_Folder, bg='black', activebackground='black', bd=0,
               command=self.add_music).place(x=300, y=y_base)

        self.Button_Next = PhotoImage(file='img/buttons/next.png')
        Button(self.root, image=self.Button_Next,
               bg='black', activebackground='black', command=self.next_song, bd=0).place(x=x_base+280, y=y_base)

    # draws playlist box
    def draw_playlist(self):
        self.Frame_Music = Frame(self.root, bd=2, relief=RAISED)
        self.Frame_Music.place(x=300, y=285, width=565, height=265)

        self.Scroll = Scrollbar(self.Frame_Music, width=10, bg='white',
                                activebackground='grey', highlightcolor='yellow')
        self.Playlist = Listbox(self.Frame_Music, width=100, height=20, font=('courier new', 10), bg='#004aad',
                                     fg='white', selectbackground='#5de0e6', cursor='hand2', bd=0, yscrollcommand=self.Scroll.set)

        self.progress_pos = IntVar()
        self.Progressbar = ttk.Progressbar(
            self.Frame_Music, style='black.Horizontal.TProgressbar', length=565, mode='determinate', orient='horizontal', variable=self.progress_pos)
        self.Progressbar.grid(column=0, row=0, columnspan=2, padx=10, pady=20)
        self.Progressbar.pack()

        self.Scroll.config(command=self.Playlist.yview)
        self.Scroll.pack(side=RIGHT, fill=Y)
        self.Playlist.pack(side=LEFT, fill=BOTH)


    # draws background image
    def draw_background(self):
        self.Background = PhotoImage(file='img/background.png')
        Label(self.root, image=self.Background, bg='#2596be').pack()

    # controls play button
    def play_music(self):
        if self.paused:
            self.control_pause()
        else:
            self.Playlist.focus()
            active_song = self.Playlist.get(ACTIVE)
            self.curr_song = self.Playlist.index(ACTIVE)
            mixer.music.load(active_song)
            self.song = mp3.MP3(active_song)
            self.Progressbar.configure(maximum=self.song.info.length*20)
            self.reset_progressbar()
            self.start_progressbar()
            mixer.music.play()

    # controls pause button
    def control_pause(self):
        if self.paused:
            self.start_progressbar()
            mixer.music.unpause()
        else:
            self.stop_progressbar()
            mixer.music.pause()
        self.paused = not self.paused

    # controls stop button
    def stop_music(self):
        self.stop_progressbar()
        self.reset_progressbar()
        mixer.music.stop()

    # controls next button
    def next_song(self):
        self.Playlist.focus()
        index = self.Playlist.index(ACTIVE)

        self.curr_song = self.Playlist.index(
            ACTIVE) + 1 if index < len(self.song_files)-1 else 0
        self.Playlist.activate(self.curr_song)
        self.play_music()

    # controls previous song button
    def prev_song(self):
        self.Playlist.focus()
        index = self.Playlist.index(ACTIVE)
        self.curr_song = index - 1 if index > 0 else len(self.song_files) - 1
        self.Playlist.activate(self.curr_song)
        self.play_music()

    # queues the next song and if no next song, the first song on the list
    def queue_music(self):
        if self.curr_song < len(self.song_files)-1:
            mixer.music.queue(self.song_files[self.curr_song+1])
        else:
            mixer.music.queue(self.song_files[0])

    # print progress position
    def song_progress(self):
        if self.Progressbar['value'] == self.Progressbar['maximum']:
            self.stop_progressbar()

    def start_progressbar(self):
        self.Progressbar.start()

    def stop_progressbar(self):
        self.Progressbar.stop()

    def reset_progressbar(self):
        self.progress_pos.set(0)

    def get_name(self, name):
        r = name.replace('-', ' ')
        return r[:-11]