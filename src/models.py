from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def get_monday():
    now = datetime.now(tz=ZoneInfo('Europe/Skopje'))
    return now - timedelta(days=now.weekday())


class TimeAdjuster:
    __instance = None
    __trans_dict = {'понеделник': 0,
                    'вторник': 1,
                    'среда': 2,
                    'четврток': 3,
                    'петок': 4
                    }
    __monday = get_monday()

    @staticmethod
    def adjust(day,time):
        weekday=TimeAdjuster.__trans_dict[day]
        tmp=TimeAdjuster.__monday + timedelta(days=weekday)
        return tmp.replace(hour=time.hour,minute=time.minute,second=0)

    @staticmethod
    def instance():
        if TimeAdjuster.__instance is None:
            TimeAdjuster.__instance = TimeAdjuster()
        return TimeAdjuster.__instance


class Subject:
    def __init__(self, name, profs, place, start, end, day):
        self.name = name
        self.profs = profs
        self.place = place
        self.start = TimeAdjuster.adjust(day,start)
        self.end = TimeAdjuster.adjust(day,end)
        self.day=day

    def __str__(self):
        return f'{self.name} / {self.day} / {self.start.time()} - {self.end.time()}'
