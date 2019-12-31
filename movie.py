import re
import csv
import os
from imdb import IMDb
from config import csv_database_file_path as database


class Movie:
    imdb = IMDb()

    def __init__(self, path):
        self.name = self.get_movie_name(path)
        self.year = self.get_movie_year(path)
        self.path = path
        self.imdb_movie = self.get_movie_imdb_information(self.name, self.year)
        print(self.name, self.imdb_movie['rating'])

    @staticmethod
    def get_movie_name(path):
        name = ''
        a = str(path).split('\\')
        b = a[len(a) - 1].replace('.', ' ')
        c = b.split()
        name += c[0]
        c.remove(c[0])
        for d in c:
            if (d.isdigit() and len(c) >= 2) or d.startswith('('):
                break
            name += ' ' + d
        return name

    @staticmethod
    def get_movie_year(path):
        pattern = r"(19[0-9][0-9]|20[0-9][0-9])"
        year = re.findall(pattern, path)[0]
        return year

    @staticmethod
    def get_movie_imdb_information(name, year):
        movies = Movie.imdb.search_movie_advanced(name)
        for movie in movies:
            try:
                if movie['year'] == year:
                    return Movie.imdb.get_movie(movie.getID())
            except:
                continue
        return Movie.imdb.get_movie(movies[0].getID())


def update_movie_list():
    from config import movies_directories as dirs
    from config import possible_extensions

    def get_movie_in_dir(root):
        m_l = []
        files = os.listdir(root)
        for file in files:
            path = f'{root}' + '\\' + f'{file}'
            try:  # Directory
                if not file.startswith('.'):
                    get_movie_in_dir(path)
            except NotADirectoryError:  # File
                for extension in possible_extensions:
                    if file.endswith('.' + extension):
                        m_l.append(Movie(path))
        return m_l

    movie_list = get_movie_in_dir(dirs[0])
    for i in movie_list:
        print(i.name, i.year)


if __name__ == '__main__':
    update_movie_list()
