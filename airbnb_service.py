import re
import quickstart
import os.path
from pprint import pprint
import datetime
from datetime import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO, SU

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
            # print('SUMMARY----->:', calendar_list_entry['summaryOverride'], 'BNB_CALS:', cals)
            calendar_ids.append(cals)
        elif 'group.calendar' in cals:
            # print('SUMMARY----->:', calendar_list_entry['summary'], 'PER_CALS:', cals)
            cal_summary.append(calendar_list_entry['summary'])
            personal_cal_ids.append(cals)
    return calendar_ids, personal_cal_ids

get_cal_ids()

# Get data for each event
def get_eventData():
    service = cal_data[1]
    data_lst = []
    cal_id = calendar_ids
    # while True:
        
    for cal_ids in cal_id:
        events_result = service.events().list(calendarId=cal_ids, timeMin=start_date, timeMax=end_date, singleEvents=True, orderBy='startTime').execute()
    
        events = events_result.get('items', [])
        for event in events:
            data = cal_ids, event['iCalUID'], event['end'].get('dateTime', event['end'].get('date')), event['start'].get('dateTime', event['start'].get('date'))
            data_lst.append(data)
    return data_lst
        
# pprint(get_eventData())
    
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
    service = cal_data[1]
    for vals in event_values:
        if vals[0] == calendar_ids[0]:
            FP308_resource = import_data(cal_summary[1], vals[3], vals[2], vals[1])
            imported_event = service.events().import_(calendarId=personal_cal_ids[1], body=FP308_resource).execute()
            print('FP308:', personal_cal_ids[1])
            print(FP308_resource)
        elif vals[0] == calendar_ids[1]:
            MS307_resource = import_data(cal_summary[0], vals[3], vals[2], vals[1])
            imported_event = service.events().import_(calendarId=personal_cal_ids[0], body=MS307_resource).execute()
            print('MS308:', personal_cal_ids[0])
            print(MS307_resource)
        elif vals[0] == calendar_ids[2]:
            NL461_resource = import_data(cal_summary[3], vals[3], vals[2], vals[1])
            imported_event = service.events().import_(calendarId=personal_cal_ids[3], body=NL461_resource).execute()
            print('NL461:', personal_cal_ids[3])
            print(NL461_resource)
        elif vals[0] == calendar_ids[3]:
            HS407_resource = import_data(cal_summary[2], vals[3], vals[2], vals[1])
            imported_event = service.events().import_(calendarId=personal_cal_ids[2], body=HS407_resource).execute()
            print('HS407:', personal_cal_ids[2])
            print(HS407_resource)
        else:
            'No data!'
                
        
# pprint(import_event())
print('---------------------------------------------------------')

#calendar_ids[0]

def calculate_total():

    event_values = get_eventData()
    total_cost = 0
    for apt in event_values:
        # FP308
        if apt[0] == calendar_ids[0]:
            print(cal_summary[1] + ' - Start:', apt[3], 'End:', apt[2])
            total_cost += 60
        # NL461
        elif apt[0] == calendar_ids[3]:
            print(cal_summary[3] + ' - Start:', apt[3], 'End:', apt[2])
            total_cost += 50
        # MS307
        elif apt[0] == calendar_ids[2]:
            print(cal_summary[0] + ' - Start:', apt[3], 'End:', apt[2])
            total_cost += 45
        # HS407
        elif apt[0] == calendar_ids[1]:
            print(cal_summary[2] + ' - Start:', apt[3], 'End:', apt[2])
            total_cost += 45
        else:
            total_cost += 0
    return 'Total: ' + str(total_cost)
    
print('Total:', calculate_total())

#import_event()
