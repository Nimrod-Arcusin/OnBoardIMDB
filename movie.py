class Movie:
    def __init__(self, path):
        self.name = self.get_movie_name(path)
        self.path = path

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
