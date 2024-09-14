from datetime import datetime, time, date
from teacher import Teacher


class ScheduleEvent:
    def __init__(self, subject: str, format: str, start_time: time, end_time: time,
                 start_date: date, teachers: list[Teacher | str] = None, location: str = None,
                 frequency_of_weeks: int = 1):
        self.subject = subject
        self.format = format
        self.start_time = start_time
        self.end_time = end_time
        self.frequency_of_weeks = frequency_of_weeks
        self.start_date = start_date
        self.location = location
        self.teachers: list[Teacher] = []
        if teachers is not None:
            self.teachers = [teacher if isinstance(teacher, Teacher) else Teacher(teacher) for teacher in teachers]

    def __str__(self):
        res = (f'\n[{self.format}] {self.subject.upper()}\n'
               f'{self.start_time.strftime("%H:%M")} - {self.end_time.strftime("%H:%M")}\n')
        if self.location:
            res += f'{self.location}\n'
        if not self.teachers:
            return res
        for teacher in self.teachers:
            res += f'{teacher.name},\n'
        return res[:-2] + '\n'

    def __repr__(self):
        return self.__str__() + f'frequency_of_weeks: {self.frequency_of_weeks}\nstart_day: {self.start_date}\n'

    def __lt__(self, other):
        return datetime.combine(self.start_date, self.start_time) < datetime.combine(other.start_date, other.start_time)
