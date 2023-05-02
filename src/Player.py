import os
from tkinter import *
from tkinter import Tk, ttk
from tkinter import filedialog
from pygame import mixer
from mutagen import mp3
import json


class Player:
    def __init__(self):
        self.paused = False
        self.btns_filepath = 'txt/btns.json'
        self.preferences_filepath = 'txt/preferences.json'
        self.preferences = {}
        self.songs = []
        self.song = None
        self.curr_song = 0
        self.cont = True

        with open(self.preferences_filepath) as pref_file:
            content = json.load(pref_file)
            if content:
                self.preferences = content

        self.loop()

    # creates app root
    def create_root(self):
        root = Tk()
        root.title("Museic")
        root.geometry("920x600+290+85")
        root.configure(background='#76b5c5')
        root.resizable(False, False)
        return root

    def draw_window(self, root):
        self.draw_background(root)
        self.draw_buttons(root)
        self.draw_playlist(root)

    def update(self, root):
        self.song_progress()
        root.after(100, lambda: self.update(root))

    def loop(self):
        root = self.create_root()
        mixer.init()

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('black.Horizontal.TProgressbar', foreground='black', background='black')
        self.draw_window(root)

        if self.preferences['path']:
            self.get_music(self.preferences['path'])
            self.queue_music()

        root.after(1000, lambda: self.update(root))
        root.mainloop()

    # loads latest playlist from json file
    def get_music(self, path):
        os.chdir(path)
        self.songs = os.listdir(path)
        for song in self.songs:
            if song.endswith('.mp3'):
                self.Area_Playlist.insert(END, song)
        self.queue_music()

    # opens file dialog and gets path to folder,
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

    # creates the buttons to control actions
    def draw_buttons(self, root):
        y_base = 220
        x_base = 533
        self.Button_Play = PhotoImage(
            file='img/buttons/play.png')
        Button(root, image=self.Button_Play, bg='black', activebackground='black', bd=0,
               command=self.play_music).place(x=x_base, y=y_base)

        self.Button_Stop = PhotoImage(file='img/buttons/stop.png')
        Button(root, image=self.Button_Stop, bg='black', activebackground='black', bd=0,
               command=self.stop_music).place(x=x_base+220, y=y_base)

        self.Button_Previous = PhotoImage(file='img/buttons/previous.png')
        Button(root, image=self.Button_Previous,
               bg='black', activebackground='black', command=self.prev_song, bd=0).place(x=x_base + 100, y=y_base)

        self.Button_Pause = PhotoImage(file='img/buttons/pause.png')
        Button(root, image=self.Button_Pause, bg='black', activebackground='black', bd=0,
               command=self.control_pause).place(x=x_base+160, y=y_base)

        self.Button_Folder = PhotoImage(file='img/buttons/folder.png')
        Button(root, image=self.Button_Folder, bg='black', activebackground='black', bd=0,
               command=self.add_music).place(x=300, y=y_base)

        self.Button_Next = PhotoImage(file='img/buttons/next.png')
        Button(root, image=self.Button_Next,
               bg='black', activebackground='black', command=self.next_song, bd=0).place(x=x_base+280, y=y_base)

    # draws playlist box
    def draw_playlist(self, root):
        self.Frame_Music = Frame(root, bd=2, relief=RAISED)
        self.Frame_Music.place(x=300, y=285, width=565, height=265)

        self.Scroll = Scrollbar(self.Frame_Music, width=13, bg='white',
                                activebackground='grey', highlightcolor='yellow')
        self.Area_Playlist = Listbox(self.Frame_Music, width=100, font=('courier new', 10), bg='#004aad',
                                     fg='white', selectbackground='#5de0e6', cursor='hand2', bd=0, yscrollcommand=self.Scroll.set)

        self.progress_pos = IntVar()
        self.Progressbar = ttk.Progressbar(
            self.Frame_Music, style='black.Horizontal.TProgressbar', length=565, mode='determinate', orient='horizontal', variable=self.progress_pos)
        self.Progressbar.grid(column=0, row=0, columnspan=2, padx=10, pady=20)
        self.Progressbar.pack()

        self.Scroll.config(command=self.Area_Playlist.yview)
        self.Scroll.pack(side=RIGHT, fill=Y)
        self.Area_Playlist.pack(side=LEFT, fill=BOTH)

    # draws background image
    def draw_background(self, root):
        self.Background = PhotoImage(file='img/background.png')
        Label(root, image=self.Background, bg='#2596be').pack()

    # controls play button
    def play_music(self):
        self.Area_Playlist.focus()
        active_song = self.Area_Playlist.get(ACTIVE)
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
        self.Area_Playlist.focus()
        index = self.Area_Playlist.index(ACTIVE)
        self.curr_song = self.Area_Playlist.index(
            ACTIVE) + 1 if index < len(self.songs) else 0
        self.Area_Playlist.activate(self.curr_song)
        self.play_music()

    # controls previous song button
    def prev_song(self):
        self.Area_Playlist.focus()
        index = self.Area_Playlist.index(ACTIVE)
        self.curr_song = index - 1 if index > 0 else len(self.songs) - 1
        self.Area_Playlist.activate(self.curr_song)
        self.play_music()

    # sets queue
    def queue_music(self):
        for song in self.songs:
            if song.endswith('.mp3'):
                mixer.music.queue(song)

    # print progress position
    def song_progress(self):
        if self.Progressbar['value'] < self.Progressbar['maximum']:
            print(self.Progressbar['value'])
        else:
            print('completed')

    def start_progressbar(self):
        self.Progressbar.start()

    def stop_progressbar(self):
        self.Progressbar.stop()

    def reset_progressbar(self):
        self.progress_pos.set(0)