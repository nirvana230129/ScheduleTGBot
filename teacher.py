import os


class Teacher:
    def __init__(self, name: str, db_file='data/teachers.txt', photos_dir='data/photos/', extension='.jpg'):
        self.name: str | None = None
        self.photo: str | None = None
        self.link: str | None = None
        self.subjects: list[str] | None = None

        surname = split_name(name.strip())[0]
        with open(db_file) as file:
            for teacher in eval(file.read()):
                if teacher['name'].startswith(surname):
                    self.name = teacher['name']
                    self.link = teacher['link']

                    last_name, *other_parts = split_name(self.name)
                    self.photo = photos_dir + '_'.join((last_name, *[part[0] for part in other_parts])) + extension
                    if not os.path.isfile(self.photo):
                        self.photo = None

                    return
        raise KeyError(f'No such teacher: {self.name}')

    def __str__(self):
        return f'name: {self.name}\nphoto: {self.photo}\nlink: {self.link}'

    def __repr__(self):
        return self.name


def split_name(name: str) -> list[str]:
    to_replace = []
    for l in name.lower():
        if not l.isalpha():
            to_replace.append(l)
    for l in to_replace:
        name = name.replace(l, ' ')
    while '  ' in name:
        name = name.replace('  ', ' ')
    return name.split()
