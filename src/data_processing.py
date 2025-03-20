from bs4 import BeautifulSoup
from .validation import ValidTimes,ValidDaysCheck
from .models import Subject
from datetime import datetime,time

def get_x_for_subject(sub_text):
    try:
        return float(sub_text['x'])
    except:
        return float(sub_text.contents[0]['x'])

def parse_time(time_el):
    time_format='%H:%M'
    start,end=time_el.split("-")
    start,end=start.strip(),end.strip()
    return datetime.strptime(start,time_format).time(), \
        datetime.strptime(end,time_format).time()

def extract_dates(text_coll):
    ch_time=ValidTimes()
    ch_days=ValidDaysCheck()

    sorted_days = []  # (x,text)
    sorted_times = []  # (y,text)
    i_end_time=None
    for i in range(1, len(text_coll)):
        el=text_coll[i]
        txt_el=el.get_text()
        if ch_days.check(txt_el):
            sorted_days.append((
                float(el.next_sibling['x']),
                txt_el
            ))
        elif ch_time.check(txt_el):
            sorted_times.append((
                float(el.next_sibling['y']),
                parse_time(txt_el)
            ))
        else:
            i_end_time=i
            break

    return sorted_days, sorted_times, i_end_time

"""
Find the maximum of all the min elements in a scheudle array.
"""
def binary_search(arr,coord):
    left=-1
    right=len(arr)
    result=None
    while (right-left)>1:
        mid=(left+right)//2
        if arr[mid][0]>coord:
            right=mid-1
        else:
            result=arr[mid]
            left=mid+1
    return result

def extract_subjects(sorted_days, sorted_times, i_start ,text_coll):
    PROFS_DELIMITER='/'
    subs=[]
    for i in range(i_start, len(text_coll),3):
        sub_name=text_coll[i].get_text()
        sub_profs=text_coll[i+1].get_text().split(PROFS_DELIMITER)
        place=text_coll[i+2].get_text()

        day=binary_search(sorted_days,get_x_for_subject(text_coll[i]))[1]
        # time=binary_search(sorted_times,float(text_coll[i]['y']))[1]

        tmp=datetime.now().time()
        subs.append(
            Subject(
                 sub_name, sub_profs, place, tmp,tmp , day
            )
        )
    return subs
#143.97

def process():
    I_VALIDITY_TEXT=-3
    I_METADATA_TEXT=I_VALIDITY_TEXT

    with open('./src/index.html', 'r') as f:
        timetable = BeautifulSoup(f.read(), 'html.parser')
        timetable=timetable.find_all('text')
        # validity_text=timetable[I_VALIDITY_TEXT]
        timetable=timetable[:I_METADATA_TEXT]
        sorted_days, sorted_times, i_end_time=extract_dates(timetable)
        [print(sub) for sub in extract_subjects(sorted_days, sorted_times, i_end_time, timetable)]
