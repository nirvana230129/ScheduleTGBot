from datetime import datetime, time, date
from teacher import Teacher


class ScheduleEvent:
    def __init__(self, subject: str, start_time: time, end_time: time,
                 start_date: date, format: str = None, teachers: list[Teacher | str] = None, location: str = None,
                 frequency_of_weeks: int = 1):
        self.subject = subject
        self.start_time = start_time
        self.end_time = end_time
        self.start_date = start_date
        self.format = format
        self.teachers: list[Teacher] = []
        if teachers is not None:
            self.teachers = [teacher if isinstance(teacher, Teacher) else Teacher(teacher) for teacher in teachers]
        self.location = location
        self.frequency_of_weeks = frequency_of_weeks

    def __str__(self):
        res = '\n'
        if self.format is not None:
            res += f'[{self.format}] '
        res += f'{self.subject.upper()}\n{self.start_time.strftime("%H:%M")} - {self.end_time.strftime("%H:%M")}\n'
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
