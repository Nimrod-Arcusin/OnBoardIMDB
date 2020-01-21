import subprocess
import movie
import time
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from functools import partial
from threading import Thread

update_database_thread = Thread(target=movie.update_database)
update_database_thread.start()


class App:
    def __init__(self, root):
        from config import cover_size, covers_in_line, covers_in_row, default_sorting_type
        self.cover_size = cover_size
        self.covers_in_line = covers_in_line
        self.covers_in_row = covers_in_row

        # win config
        self.main_win = root
        self.main_win.title('On Board IMDB')
        self.main_win.resizable(False, True)

        self.movies_list = []
        self.update_movies_list()

        self.sort_type = default_sorting_type
        self.sort_by_type()

        self.covers = []

        self.app_sizing()
        self.create_top_frame()
        self.create_movies_frame()

    def update_movies_list(self):
        # getting all the movies from the database
        self.movies_list = movie.get_movies_list()
        while not self.movies_list:
            print('empty database')
            self.movies_list = movie.get_movies_list()
            time.sleep(1)

    def sort_by_type(self):
        if self.sort_type == 'rating':
            self.movies_list.sort(key=lambda x: x.rating, reverse=True)
        elif self.sort_type == 'date':
            self.movies_list.sort(key=lambda x: x.date, reverse=True)
        elif self.sort_type == 'name':
            self.movies_list.sort(key=lambda x: x.name)
        elif self.sort_type == 'year':
            self.movies_list.sort(key=lambda x: x.year, reverse=True)

    def app_sizing(self):
        """resizing window if there is not enough movies"""
        if len(self.movies_list) < self.covers_in_line:
            self.covers_in_line = len(self.movies_list)
            self.covers_in_row = 1
        elif len(self.movies_list) <= (2 * self.covers_in_line):
            self.covers_in_row = 2

    def create_top_frame(self):
        frame_top = Frame(self.main_win)
        frame_top.pack(side=TOP)
        button_update = Button(frame_top, text="sort by name", command=lambda: self.change_sorting_type('name'))
        button_update.pack(side=LEFT)
        button_update = Button(frame_top, text="sort by rating", command=lambda: self.change_sorting_type('rating'))
        button_update.pack(side=LEFT)
        button_update = Button(frame_top, text="sort by date", command=lambda: self.change_sorting_type('date'))
        button_update.pack(side=LEFT)
        button_update = Button(frame_top, text="sort by year", command=lambda: self.change_sorting_type('year'))
        button_update.pack(side=LEFT)

    def create_movies_frame(self):
        self.frame_main = Frame(self.main_win)
        self.frame_main.pack(side=TOP)
        self.frame_canvas = Frame(self.frame_main)
        self.frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
        self.frame_canvas.grid_rowconfigure(0, weight=1)
        self.frame_canvas.grid_columnconfigure(0, weight=1)
        self.frame_canvas.grid_propagate(False)

        # Add a canvas in that frame
        self.canvas = Canvas(self.frame_canvas, bg="black")
        self.canvas.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        vsb = Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=vsb.set)

        # Create a frame to contain the buttons
        self.frame_buttons = Frame(self.canvas)
        self.frame_buttons.clipboard_clear()
        self.canvas.create_window((0, 0), window=self.frame_buttons, anchor='nw')

        self.covers = []
        self.open_movie_funcs = []
        for i in range(len(self.movies_list)):
            self.covers.append(self.movies_list[i].cover)
            print(self.movies_list[i].name)
            self.covers[i].thumbnail(self.cover_size, Image.ANTIALIAS)
            self.covers[i] = ImageTk.PhotoImage(self.covers[i])
            self.open_movie_funcs.append(partial(self.open_movie, self.movies_list[i].path))

        self.buttons = []
        for i in range(len(self.movies_list)):
            self.buttons.append(Button(self.frame_buttons, text=self.movies_list[i].name, image=self.covers[i],
                                       command=self.open_movie_funcs[i]))
            self.buttons[i].grid(row=i // self.covers_in_line, column=i % self.covers_in_line, sticky='news')

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.frame_buttons.update_idletasks()

        # Resize the canvas frame to show buttons and the scrollbar
        self.frame_canvas.config(
            width=sum([self.buttons[j].winfo_width() for j in range(0, self.covers_in_line)]) + vsb.winfo_width(),
            height=int(self.cover_size[1] * self.covers_in_row))

        # Set the canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    @staticmethod
    def open_movie(path):
        """
        function that open a movie from path in the player from the config file
        :return: noting
        """
        from config import player_path
        subprocess.Popen([player_path, path])

    def update_screen(self):
        self.update_movies_list()
        self.sort_by_type()
        self.app_sizing()
        # self.frame_buttons.destroy()
        # self.canvas.destroy()
        # self.frame_canvas.destroy()
        self.frame_main.destroy()
        self.create_movies_frame()
        self.main_win.update()

    def change_sorting_type(self, sort_type):
        self.sort_type = sort_type
        self.update_screen()


root = Tk()
app = App(root)
root.mainloop()