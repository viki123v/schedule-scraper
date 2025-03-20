import re

class ValidDaysCheck:
    def __init__(self):
        self._valid = {'понеделник',
                       'вторник',
                       'среда',
                       'четврток',
                       'петок'
                       }

    def check(self, text):
        return text.lower() in self._valid

class ValidTimes:
    def __init__(self):
        self._re = re.compile(r'\s*\d{1,2}:\d{1,2}\s?-\s?\d{1,2}:\d{1,2}\s*')

    def check(self,text):
        return self._re.match(text) is not None