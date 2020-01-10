import subprocess
import movie
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from config import cover_size, covers_in_line, player_path
from functools import partial
from threading import Thread

update_database_thread = Thread(target=movie.update_database)
update_database_thread.start()
movies_list = movie.get_movies_list()


def open_movie(path):
    subprocess.Popen([player_path, path])


main_win = Tk()
main_win.title('On Board IMDB')
main_win.resizable(False, False)

main_win.style = Style().configure('TButton', background='black')

frame_main = Frame(main_win)
frame_main.grid(sticky='news')
frame_canvas = Frame(frame_main)
frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)
frame_canvas.grid_propagate(False)

# Add a canvas in that frame
canvas = Canvas(frame_canvas, bg="black")
canvas.grid(row=0, column=0, sticky="news")

# Link a scrollbar to the canvas
vsb = Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
vsb.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=vsb.set)

# Create a frame to contain the buttons
frame_buttons = Frame(canvas)
canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

covers = []
open_movie_funcs = []
for i in range(len(movies_list)):
    covers.append(movies_list[i].cover)
    covers[i].thumbnail(cover_size, Image.ANTIALIAS)
    covers[i] = ImageTk.PhotoImage(covers[i])
    open_movie_funcs.append(partial(open_movie, movies_list[i].path))

buttons = []
for i in range(len(movies_list)):
    buttons.append(Button(frame_buttons, text=movies_list[i].name, image=covers[i],
                          command=open_movie_funcs[i]))
    buttons[i].grid(row=i // covers_in_line, column=i % covers_in_line, sticky='news')

# Update buttons frames idle tasks to let tkinter calculate buttons sizes
frame_buttons.update_idletasks()

# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
frame_canvas.config(width=sum([buttons[j].winfo_width() for j in range(0, covers_in_line)]) + vsb.winfo_width(),
                    height=int(cover_size[1] * 2.5))

# Set the canvas scrolling region
canvas.config(scrollregion=canvas.bbox("all"))

main_win.mainloop()
