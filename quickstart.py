from __future__ import print_function
import datetime
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
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    calendar_ids = []
    
    # Get all Airbnb calendar id's
    def get_cal_ids():
        page_token = None
        
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                cals = calendar_list_entry['id']
                if "import.calendar" in cals:
                    calendar_ids.append(cals)
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        return calendar_ids
    
    # Get data for each event
    def get_eventData():
        page_token = None
        data_lst = []
        calendar_ids = get_cal_ids()
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for cal_ids in calendar_ids:
                events_result = service.events().list(calendarId=cal_ids, maxResults=3,timeMin=now, singleEvents=True, orderBy='startTime').execute()

                events = events_result.get('items', [])
                
                for event in events:
                    data = cal_ids, event['iCalUID'], event['end'].get('dateTime', event['end'].get('date')), event['start'].get('dateTime', event['start'].get('date'))
                    data_lst.append(data)
            return data_lst

    # Imports private copy of event
    def import_event():
        event_values = get_eventData()
        data_len = len(event_values)
        summary = ''
        print(event_values[0])
        for vals in event_values:
            for _ids in calendar_ids:
                if _ids == calendar_ids[0]:
                    summary = 'FP308'
                elif _ids == calendar_ids[1]:
                    summary = 'MS307'
                elif _ids == calendar_ids[2]:
                    summary = 'NL461'
                elif _ids == calendar_ids[3]:
                    summary = 'HS407'
                else:
                    'No data!'

                _resource = {
                    'summary': f'{summary}',
                    'start': {
                        'date': vals[3]
                    },
                    'end': {
                        'date': vals[2]
                    },
                    'iCalUID': vals[1]
                }
                # imported_event = service.events().import_(calendarId='primary', body=event).execute()
                data_len -= 1
                pprint.pprint(_resource)
        
    print(import_event())
    print('---------------------------------------------------------')

    
if __name__ == '__main__':
    main()
