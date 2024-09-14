from icalendar import Calendar, Event
from datetime import datetime, date, timedelta

from teacher import Teacher
from schedule_event import ScheduleEvent


class Schedule:
    def __init__(self, file_path: str):
        self._all_events: list[ScheduleEvent] = []
        self._all_teachers: list[Teacher] = []

        if file_path[file_path.rfind('.') + 1:] == 'ics':
            self._read_ics(file_path)
        elif file_path[file_path.rfind('.') + 1:] == 'txt':
            self._read_txt(file_path)
        self._all_events.sort()

        self.first_day = self._all_events[0].start_date
        self._even_week: list[ScheduleEvent] = []
        self._odd_week: list[ScheduleEvent] = []
        self._distribute_by_week()

    def _read_txt(self, file_path: str):
        with (open(file_path, encoding='utf-8') as file):
            for component in eval(file.read()):
                teachers = []
                for teacher_name in component['teachers']:
                    teacher = self.get_teacher(teacher_name)
                    if teacher is None:
                        teacher = Teacher(teacher_name)
                        self._all_teachers.append(teacher)
                    teachers.append(teacher)
                start_dt = datetime(*component['start_dt'])
                self._all_events.append(ScheduleEvent(
                    component['subject'],
                    component['format'],
                    start_dt.time(),
                    datetime(*component['end_dt']).time(),
                    start_dt.date(),
                    teachers,
                    component['location'],
                    component['frequency_of_weeks']))

    def _distribute_by_week(self):
        for i, event in enumerate(self._all_events):
            if event.frequency_of_weeks == 1:
                self._even_week.append(event)
                self._odd_week.append(event)
            elif (event.start_date - self.first_day).days < 7:
                self._odd_week.append(event)
            else:
                self._even_week.append(event)
        self._even_week.sort()

    def print_events(self, events: list[ScheduleEvent] = None):
        print(len(events or self._all_events))
        for event in events or self._all_events:
            print(event)

    def get_teacher(self, name: str) -> Teacher | None:
        name = name.lower().strip()
        for teacher in self._all_teachers:
            if teacher.name.lower().startswith(name):
                return teacher
        return None
