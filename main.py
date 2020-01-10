import os

import movie
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from config import covers_path as covers_path

cover_size = (200, 300)
covers_in_line = 7

# movie.update_database()
movies_list = movie.get_movies_list()
print(list(map(lambda x: x.id, movies_list)))

main_win = Tk()
main_win.title('On Board IMDB')
movie_buttons = []

# for i in range(len(movie_buttons)):
#     pic = movies_list[i].cover
#     print(pic)
#     pic.thumbnail(pic_size, Image.ANTIALIAS)
#     movie_buttons[i].config(image=ImageTk.PhotoImage(pic))

covers = []

for i in range(len(movies_list)):
    covers.append(movies_list[i].cover)
    covers[i].thumbnail(cover_size, Image.ANTIALIAS)
    covers[i] = ImageTk.PhotoImage(covers[i])

for i in range(len(movies_list)):
    movie_buttons.append(Button(main_win, text='hello', image=covers[i]))
    movie_buttons[i].grid(row=i // covers_in_line, column=i % covers_in_line)
    print(i)

main_win.update()
main_win.resizable(False, False)
main_win.mainloop()
