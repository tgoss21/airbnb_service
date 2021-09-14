import re
import sqlite3
import pandas as pd
from datetime import datetime
import quickstart
# from __future__ import print_function
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO, SU
import os.path
import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import quickstart



FP308_id = 'mu04c7ugregh71cdbp6jij6522j4paev@import.calendar.google.com'
MS307_id = 'ggr7r4l0c2aog6t6lfbmotp6b9vg6gi9@import.calendar.google.com'
NL461_id = 'jorp1cu13a8a9p3s40qimcl61ijfh2tp@import.calendar.google.com'
HS407_id = 'mkclgiicomv8fg042k3262osmtevi4qk@import.calendar.google.com'
today = datetime.today()
start = today - relativedelta(weekday=MO(-1))
end = today - relativedelta(weekday=SU(1))
end_date = end.isoformat('T') + "Z"
start_date = start.isoformat('T') + "Z"

cal_data = quickstart.Quickstart.main()
calendar_ids = []
personal_cal_ids = []
cal_summary = []


# Get all Airbnb calendar id's
def get_cal_ids():

    for calendar_list_entry in cal_data[0]:
        cals = calendar_list_entry['id']
        if "import.calendar" in cals:
            print('SUMMARY----->:', calendar_list_entry['summaryOverride'], 'BNB_CALS:', cals)
            calendar_ids.append(cals)
        elif 'group.calendar' in cals:
            print('SUMMARY----->:', calendar_list_entry['summary'], 'PER_CALS:', cals)
            cal_summary.append(calendar_list_entry['summary'])
            personal_cal_ids.append(cals)
    return calendar_ids, personal_cal_ids

get_cal_ids()

# Get data for each event
def get_eventData():
    service = cal_data[1]
    data_lst = []
    cal_id = calendar_ids
    while True:
        
        for cal_ids in cal_id:
            events_result = service.events().list(calendarId=cal_ids, timeMin=start_date, timeMax=end_date, singleEvents=True, orderBy='startTime').execute()
    
            events = events_result.get('items', [])
            for event in events:
                data = cal_ids, event['iCalUID'], event['end'].get('dateTime', event['end'].get('date')), event['start'].get('dateTime', event['start'].get('date'))
                data_lst.append(data)
        return data_lst
        
# pprint.pprint(get_eventData())
    
def import_data(summary, start, end, iCalUID):
    _resource = {
                'summary': summary,
                    'start': {
                        'date': start
                    },
                    'end': {
                        'date': end
                    },
                    'iCalUID': iCalUID
                }
    return _resource

    # Imports private copy of event
def import_event():
    event_values = get_eventData()
        
    for vals in event_values:
        if vals[0] == calendar_ids[0]:
            FP308_resource = import_data(cal_summary[1], vals[3], vals[2], vals[1])
            # imported_event = service.events().import_(calendarId=personal_cal_ids[1], body=FP308_resource).execute()
            print('FP308:', personal_cal_ids[1])
            print(FP308_resource)
        elif vals[0] == calendar_ids[1]:
            MS307_resource = import_data(cal_summary[0], vals[3], vals[2], vals[1])
            # imported_event = service.events().import_(calendarId=personal_cal_ids[0], body=MS307_resource).execute()
            print('MS308:', personal_cal_ids[0])
            print(MS307_resource)
        elif vals[0] == calendar_ids[2]:
            NL461_resource = import_data(cal_summary[3], vals[3], vals[2], vals[1])
            # imported_event = service.events().import_(calendarId=personal_cal_ids[3], body=NL461_resource).execute()
            print('NL461:', personal_cal_ids[3])
            print(NL461_resource)
        elif vals[0] == calendar_ids[3]:
            HS407_resource = import_data(cal_summary[2], vals[3], vals[2], vals[1])
            # imported_event = service.events().import_(calendarId=personal_cal_ids[2], body=HS407_resource).execute()
            print('HS407:', personal_cal_ids[2])
            print(HS407_resource)
        else:
            'No data!'
                
        
pprint.pprint(import_event())
print('---------------------------------------------------------')





def calculate_total(cleaning_list):
    apt_lst = re.findall(r'\w+', cleaning_list)

    total_cost = 0
    for apt in apt_lst:
        if 'FP308' in apt:
            total_cost += 60
        elif 'NL461' in apt:
            total_cost += 50
        elif 'MS307' in apt:
            total_cost += 45
        elif 'HS407' in apt:
            total_cost += 45
        else:
            total_cost += 0
    return 'Total: ' + str(total_cost)


cleaning_lst = '''
    8/23: MS307 FP308 HS407
    8/24: NL461 FP308
    8/25: HS407
    8/26: MS307 HS407
    8/27: MS307 NL461
    8/28: FP308
    8/29: FP308 MS307 HS407
'''

# print(cleaning_lst + '\n Total: ' + calculate_total(cleaning_lst))


# def get_query_results():
#     conn = sqlite3.connect('/Users/tracygoss/Library/Messages/chat.db')
#     cur1 = conn.cursor()
#     cur1.execute('''SELECT datetime(m.date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") AS message_date,
#                  text
#              FROM chat c
#                 JOIN chat_message_join cmj ON c."ROWID" = cmj.chat_id
#                 JOIN message m ON cmj.message_id = m."ROWID"
#              WHERE c.chat_identifier = "+12064290405" and m.is_sent = 1
#              ORDER BY m.date DESC
#              LIMIT 10; ''')

#     results = ''
#     for message_data in cur1.fetchall():
#         print(message_data)
#         results += str(message_data)
#     return results


# text_messages = get_query_results()

# print(text_messages + '\n' + calculate_total(text_messages))
