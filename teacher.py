import os


class Teacher:
    def __init__(self, name: str, db_file='data/teachers.txt', photos_dir='data/photos/', extension='.jpg'):
        """
        :param name: full name (option with initials like 'Ivanov A.A.' is possible) of teacher
        :param db_file: file path to data about full names and links
        :param photos_dir: directory of photos
        :param extension: photos extension
        """
        self.name: str | None = None
        self.photo: str | None = None
        self.link: str | None = None
        self.subjects: list[str] = []

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
        self.name = name.strip()

    def add_subject(self, subject: str, format: str = None):
        """
        Adds subject to teacher.
        :param subject: name of subject
        :param format: lecture, laboratory or other
        """
        new_subject = ('' if format is None else f'[{format}] ') + subject
        if new_subject not in self.subjects:
            self.subjects.append(new_subject)
        self.subjects.sort()

    def __str__(self):
        return f'{self.name}\nlink: {self.link}\nПредметы:\n  ' + '\n  '.join(self.subjects) + '\n'

    def __repr__(self):
        return (f'name: {self.name}\nphoto: {self.photo}\nlink: {self.link}\nsubjects:\n  ' +
                '\n  '.join(self.subjects) + '\n')


def split_name(name: str) -> list[str]:
    """
    Splits name into parts (name, surname, etc.).
    :param name: full name of teacher
    :return: list of name parts
    """
    for l in [l for l in name.lower() if not l.isalpha()]:
        name = name.replace(l, ' ')
    while '  ' in name:
        name = name.replace('  ', ' ')
    return name.split()
