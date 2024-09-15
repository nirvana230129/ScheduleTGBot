from icalendar import Calendar
from datetime import datetime, date, timedelta

from teacher import Teacher
from schedule_event import ScheduleEvent


class Schedule:
    def __init__(self, file: str):
        """
        :param file: file with scheduled events.
        """
        self._all_events: list[ScheduleEvent] = []
        self._all_teachers: list[Teacher] = []

        if file[file.rfind('.') + 1:] == 'ics':
            self._read_ics(file)
        elif file[file.rfind('.') + 1:] == 'txt':
            self._read_txt(file)
        self._all_events.sort()

        self.first_day = self._all_events[0].start_date
        self._even_week: list[ScheduleEvent] = []
        self._odd_week: list[ScheduleEvent] = []
        self._distribute_by_week()

    def _read_ics(self, file_path: str):
        """
        Create a schedule based on the data from the .ics file.
        :param file_path: file with scheduled events
        """
        with open(file_path, encoding='utf-8') as file:
            calendar = Calendar.from_ical(file.read())
            for component in calendar.walk('VEVENT'):
                teachers = []
                teacher_names = component.get('description').replace('Б22-505', '').replace('\xa0', ' ')[:-1]
                if teacher_names:
                    for teacher_name in teacher_names.split(', '):
                        teacher = self.get_teacher(teacher_name.split()[0])
                        if teacher is None:
                            teacher = Teacher(teacher_name)
                            self._all_teachers.append(teacher)
                        teachers.append(teacher)
                        teacher.add_subject(component.get('summary'))

                self._all_events.append(ScheduleEvent(
                    component.get('summary'),
                    component.get('dtstart').dt.time(),
                    component.get('dtend').dt.time(),
                    component.get('dtstart').dt.date(),
                    teachers=teachers,
                    location=component.get('location'),
                    frequency_of_weeks=1 + int('INTERVAL' in component.get('rrule'))))

    def _read_txt(self, file_path: str):
        """
        Create a schedule based on the data from the .txt file.
        :param file_path: file with scheduled events
        """
        with (open(file_path, encoding='utf-8') as file):
            for component in eval(file.read()):
                teachers = []
                for teacher_name in component['teachers']:
                    teacher = self.get_teacher(teacher_name.split()[0])
                    if teacher is None:
                        teacher = Teacher(teacher_name)
                        self._all_teachers.append(teacher)
                    teachers.append(teacher)
                    teacher.add_subject(component['subject'], component['format'])

                start_dt = datetime(*component['start_dt'])
                self._all_events.append(ScheduleEvent(
                    component['subject'],
                    start_dt.time(),
                    datetime(*component['end_dt']).time(),
                    start_dt.date(),
                    component['format'],
                    teachers,
                    component['location'],
                    component['frequency_of_weeks']))

    def _distribute_by_week(self):
        """
        Makes a schedule for even and odd weeks.
        """
        for i, event in enumerate(self._all_events):
            if event.frequency_of_weeks == 1:
                self._even_week.append(event)
                self._even_week[-1].start_date += timedelta(days=7)
                self._odd_week.append(event)
            elif (event.start_date - self.first_day).days < 7:
                self._odd_week.append(event)
            else:
                self._even_week.append(event)
        self._even_week.sort()

    def print_events(self, events: list[ScheduleEvent] = None):
        """
        Prints events from provided list or all events from the schedule if there is no one.
        :param events: list of events to print
        """
        print(len(events or self._all_events))
        for event in events or self._all_events:
            print(event)

    def get_schedule_by_date(self, given_date: date) -> list[ScheduleEvent]:
        """
        Makes a list of events by provided date.
        :param given_date: date to get events by
        :return: list of events
        """
        if ((given_date - self.first_day).days // 7 + 1) % 2:
            return [event for event in self._odd_week if (event.start_date - given_date).days % 7 == 0]
        return [event for event in self._even_week if (event.start_date - given_date).days % 7 == 0]

    def get_schedule_for_today(self) -> list[ScheduleEvent]:
        """
        Makes a list of events for today.
        :return: list of events
        """
        return self.get_schedule_by_date(datetime.today().date())

    def get_schedule_for_tomorrow(self) -> list[ScheduleEvent]:
        """
        Makes a list of events for tomorrow.
        :return: list of events
        """
        return self.get_schedule_by_date(datetime.today().date() + timedelta(days=1))

    def get_teacher(self, name: str) -> Teacher | None:
        """
        Finds the teacher by the prefix of the name.
        :param name: prefix of the teacher name
        :return: found teacher or None if not found
        """
        name = name.lower().strip()
        for teacher in self._all_teachers:
            if teacher.name.lower().startswith(name):
                return teacher
        return None
