import os


class Teacher:
    def __init__(self, name: str, db_file='data/teachers.txt', photos_dir='data/photos/', extension='.jpg'):
        self.name: str | None = None
        self.photo: str | None = None
        self.link: str | None = None
        self.subjects: list[str] | None = None

        surname = name.strip().split()[0]
        with open(db_file) as file:
            for teacher in eval(file.read()):
                if teacher['name'].startswith(surname):
                    self.name = teacher['name']
                    self.link = teacher['link']

                    last_name, first_name, patronymic = self.name.split()
                    self.photo = photos_dir + '_'.join((last_name, first_name[0], patronymic[0])) + extension
                    if not os.path.isfile(self.photo):
                        self.photo = None

                    return
        raise KeyError(f'No such teacher: {self.name}')

    def __str__(self):
        return f'name: {self.name}\nphoto: {self.photo}\nlink: {self.link}'

    def __repr__(self):
        return self.name
