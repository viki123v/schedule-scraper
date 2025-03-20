def date_formate(start_time,end_time,day):
    return f'{start_time.isoformat()}-{end_time.isoformat()}-{day}'

class Subject:
    def __init__(self,name,profs,place,start,end,day):
        self.name=name
        self.profs=profs
        self.place=place
        self.date=date_formate(start,end,day)

    def __str__(self):
        return f'{self.name} / {self.date} / {self.place} / '