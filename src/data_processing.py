from bs4 import BeautifulSoup
from .validation import ValidTimes,ValidDaysCheck
from .models import Subject
from datetime import datetime,time

def check_tspan_els(text_el):
    if len(text_el.contents) == 0:
        return text_el.get_text()

    text_content=""
    for child in text_el.children:
        text_content += child.text + ' '
    return text_content

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
    left=0
    right=len(arr)-1
    results=None
    while left<=right:
        mid=(left+right)//2
        if arr[mid][0] > coord:
            right=mid-1
        else:
            results=arr[mid]
            left=mid+1

    if left<len(arr) and arr[left][0] <= coord:
        results=arr[left]
    return results[1]

def extract_subjects(sorted_days, sorted_times, i_start ,text_coll):
    subs=[]
    PROF_DELIMITAR='/'
    for i in range(i_start, len(text_coll),3):
        sub_name=check_tspan_els(text_coll[i])
        sub_profs=check_tspan_els(text_coll[i+1]).split(PROF_DELIMITAR)
        place=text_coll[i+2].get_text()
        rect=text_coll[i+2].next_sibling

        day=binary_search(sorted_days,float(rect['x']))
        start_time=binary_search(sorted_times,float(rect['y']))[0]
        height=float(rect['height'])
        end_time=binary_search(sorted_times,
                               float(rect['y'])+height-0.2*height)[1]

        subs.append(
            Subject(
                 sub_name, sub_profs, place, start_time,end_time , day
            )
        )
    return subs

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
