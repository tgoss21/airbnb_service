from __future__ import print_function
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO, SU
import os.path
import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']


def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/tracygoss/Desktop/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    FP308_id = 'mu04c7ugregh71cdbp6jij6522j4paev@import.calendar.google.com'
    MS307_id = 'ggr7r4l0c2aog6t6lfbmotp6b9vg6gi9@import.calendar.google.com'
    NL461_id = 'jorp1cu13a8a9p3s40qimcl61ijfh2tp@import.calendar.google.com'
    HS407_id = 'mkclgiicomv8fg042k3262osmtevi4qk@import.calendar.google.com'
    today = datetime.today()
    start = today - relativedelta(weekday=MO(-1))
    end = today - relativedelta(weekday=SU(1))
    end_date = end.isoformat('T') + "Z"
    start_date = start.isoformat('T') + "Z"
    calendar_ids = []
    personal_cal_ids = []
    cal_summary = []
    
    # Get all Airbnb calendar id's
    def get_cal_ids():
        page_token = None
        
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                cals = calendar_list_entry['id']
                if "import.calendar" in cals:
                    print('SUMMARY----->:', calendar_list_entry['summaryOverride'], 'BNB_CALS:', cals)
                    calendar_ids.append(cals)
                elif 'group.calendar' in cals:
                    print('SUMMARY----->:', calendar_list_entry['summary'], 'PER_CALS:', cals)
                    cal_summary.append(calendar_list_entry['summary'])
                    personal_cal_ids.append(cals)
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        return calendar_ids, personal_cal_ids
    
    #initalize personal and airbnb calendar lists
    get_cal_ids()

    
    # Get data for each event
    def get_eventData():
        page_token = None
        data_lst = []
        cal_id = calendar_ids
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for cal_ids in cal_id:
                events_result = service.events().list(calendarId=cal_ids, timeMin=start_date, timeMax=end_date, singleEvents=True, orderBy='startTime').execute()
    
                events = events_result.get('items', [])
                for event in events:
                    data = cal_ids, event['iCalUID'], event['end'].get('dateTime', event['end'].get('date')), event['start'].get('dateTime', event['start'].get('date'))
                    data_lst.append(data)
            return data_lst
        
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

    
if __name__ == '__main__':
    main()