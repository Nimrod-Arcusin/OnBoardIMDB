import os
from config import movies_directories as dirs
from config import possible_extensions
from movie import Movie
from imdb import IMDb

imdb = IMDb()
movie = imdb.search_movie_advanced('real steel')
print(movie[0].getID())
movie = imdb.get_movie(movie[0].getID())
for k, v in movie.items():
    print(k, v)
