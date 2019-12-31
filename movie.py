import re
import csv
import os
import time
from imdb import IMDb
from config import csv_database_file_path as database
from config import covers_path as covers


class Movie:
    imdb = IMDb()

    def __init__(self, path):
        self.name = self.get_movie_name(path)
        self.year = self.get_movie_year(path)
        self.path = path
        self.imdb_movie = self.get_movie_imdb_information(self.name, self.year)

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


def get_all_movies():
    from config import movies_directories as dirs
    from config import possible_extensions

    def get_movie_in_dir(root):
        m_l = []
        files = os.listdir(root)
        for file in files:
            path = f'{root}' + '\\' + f'{file}'
            try:  # Directory
                if not file.startswith('.'):
                    for i in get_movie_in_dir(path):
                        m_l.append(i)
            except NotADirectoryError:  # File
                for extension in possible_extensions:
                    if file.endswith('.' + extension):
                        m_l.append(path)
        return m_l

    movies_list = []
    for d in dirs:
        movies_list += get_movie_in_dir(d)
    return movies_list


def create_new_database():
    file = open(database, 'w+')
    file.write('Name,Year,Rating,Path,Genres,Plot,Cover,ID\n')
    file.close()


def download_cover(url, cover_id):
    import urllib.request
    if not os.path.exists(covers + '\\' + cover_id + '.jpg'):
        urllib.request.urlretrieve(url, covers + '\\' + cover_id + '.jpg')


def add_line_to_database(path):
    try:
        name = Movie.get_movie_name(path)
        year = Movie.get_movie_year(path)
        imdb_info = Movie.get_movie_imdb_information(name, year)
        with open(database, 'a', newline='') as csv_file:
            colons = ['Name', 'Year', 'Rating', 'Path', 'Genres', 'Plot', 'Cover', 'ID']
            csv_writer = csv.DictWriter(csv_file, fieldnames=colons)
            csv_writer.writerow(
                {'Name': name,
                 'Year': year,
                 'Rating': imdb_info['rating'],
                 'Path': path,
                 'Genres': imdb_info['genres'],
                 'Plot': imdb_info['plot'],
                 'Cover': imdb_info['full-size cover url'],
                 'ID': imdb_info.getID()})
        download_cover(imdb_info['full-size cover url'],imdb_info.getID())
        time.sleep(5)
    except:
        return


def update_database():
    if not os.path.exists(database):
        create_new_database()
    if not os.path.exists(covers):
        os.mkdir(covers)
    movies_in_dir = get_all_movies()
    movies_in_database = []
    with open(database, 'r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            movies_in_database.append(row['Path'])
    for movie in movies_in_dir:
        if movie not in movies_in_database:
            add_line_to_database(movie)


if not os.path.exists(database):
    create_new_database()

if __name__ == '__main__':
    update_database()
