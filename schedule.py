from getpass import getpass
import requests
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

BASE = "https://horizon.mcgill.ca"
referer = str()
retries = Retry(total=1000, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
session = requests.Session()
session.mount('http://', HTTPAdapter(max_retries=retries))

def get_minerva(url):
    global referer
    response = session.get(url=url, headers={'Referer':referer})
    referer = url
    return response

def post_minerva(request, url):
    global referer
    response = session.post(url=url, data=request, headers={'Referer':referer})
    referer = url
    return response

def login():
    id = input("Enter your student ID: ")
    pin = getpass(prompt="Enter your pin: ")

    get_minerva(url=BASE+"/pban1/twbkwbis.P_WWWLogin")
    post_minerva(request={'sid': id, 'PIN': pin}, url=BASE+"/pban1/twbkwbis.P_ValLogin")
    get_minerva(url=BASE+"/pban1/twbkwbis.P_GenMenu?name=bmenu.PMainMnu")

    print("Logged in sucessfully")

def formatTime(time):
    #Dealing with the pm
    if time.index(":") == 1:
        time = "0" + time
    if "pm" in time and time[:2] != "12":
        hour = int(time[:2]) + 12
        time = str(hour) + time[2:]
    time = time[:5] + ":00"
    return time

def formatDate(date):
    return datetime.strptime(date, '%b %d, %Y').isoformat()

def convertFull(time, date):
    total = f"{time}-{date}"
    datetime_object = datetime.strptime(total, '%H:%M-%b %d, %Y')
    return datetime_object.isoformat()

def getWeekday(start, target):
    start_date_obj = datetime.strptime(start, '%b %d, %Y')
    start_weekday = start_date_obj.weekday()
    days = (target - start_weekday) % 7
    new_weekday = start_date_obj + timedelta(days=days)
    return new_weekday.isoformat()

def getSchedule(semester):
    events = list()
    url = BASE + f"/pban1/bwskfshd.P_CrseSchdDetl?term_in={semester}"
    menu = get_minerva(url=url)
    data = menu.text
    soup = BeautifulSoup(data, 'html.parser')

    table_info = soup.find_all(lambda tag:tag.name == 'table' and tag['summary'] == "This layout table is used to present the schedule course detail")
    table_details = soup.find_all(lambda tag:tag.name == 'table' and tag['summary'] == "This table lists the scheduled meeting times and assigned instructors for this class..")
    for idx in range(len(table_info)):
        caption = table_info[idx].find('caption').text
        name, code, section = caption.split(" - ")
        name = name[:-1]

        table_tr = table_details[idx].find_all('tr')
        for tr in table_tr:
            table_td = tr.find_all('td')
            if not table_td:
                continue

            time = table_td[0].text
            start_time, end_time = time.split(" - ")
            start_time, end_time = formatTime(start_time), formatTime(end_time)

            weekday = table_td[1].text

            location = table_td[2].text

            date = table_td[3].text
            start_date, end_date = date.split(" - ")
            ls = "MTWRF"
            days = {ls[i]:getWeekday(start_date, i) for i in range(len(ls))}
            end_date = formatDate(end_date).replace("-", "")[:-8]
            end_date = end_date + "235959Z"

            course_type = table_td[4].text

            for day in weekday:
                start = days[day][:11] + start_time
                end = days[day][:11] + end_time

                event = {
                    'summary': f"{code} - {name} ({course_type})",
                    'description': f"Location: {location}",
                    'start': { 'dateTime': f"{start}", 'timeZone': 'EST' },
                    'end': { 'dateTime': f"{end}", 'timeZone': 'EST' },
                    'reminders': { 'useDefault': True },
                    'recurrence': [f'RRULE:FREQ=WEEKLY;UNTIL={end_date}', ],
                }

                print("Event", event)
                events.append(event)

    return events


def main():
    login()
    events = getSchedule(semester="202409")
    events.extend(getSchedule(semester="202501"))

    with open('data/schedule.json', 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=4)

    return events

if __name__ == "__main__":
    main()
