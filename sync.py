from datetime import datetime
import os.path, sys
from schedule import *

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from schedule import *

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDAR_ID = str(sys.argv[1])

def authEvent():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def addEvent(creds, data):
    try:
        for event in data:
            service = build('calendar', 'v3', credentials=creds)
            print(event)
            event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))
            print()
    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    creds = authEvent()
    data = main()
    addEvent(creds, data)
