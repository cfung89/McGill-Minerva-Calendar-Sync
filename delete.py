from datetime import datetime
import os.path, sys
from schedule import *

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from sync import authEvent

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDAR_ID = str(sys.argv[1])

def readEvent(creds):
    """Call the Calendar API"""
    eventIds = list()
    
    try:
        service = build("calendar", "v3", credentials=creds)
  
        print("Getting the upcoming events between two timeframes")
        events_result = (
            service.events()
            .list(
                calendarId=CALENDAR_ID,
                timeMin="2024-08-20T00:00:00Z",         #Change time bounds here
                timeMax="2025-04-15T00:00:00Z",
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
  
        if not events:
            print("No upcoming events found.")
            return
  
        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            eventId = event["recurringEventId"]
            if eventId not in eventIds:
                eventIds.append(eventId)
            print(start, event["summary"])
  
    except HttpError as error:
        print(f"An error occurred: {error}")

    return eventIds

def deleteEvent(creds, eventIds):
    for eventId in eventIds:
        service = build('calendar', 'v3', credentials=creds)
        service.events().delete(calendarId=CALENDAR_ID, eventId=eventId).execute()

        # instances = service.events().instances(calendarId=CALENDAR_ID, eventId=eventId).execute()
        # for instance in instances['items']:
        #     service.events().delete(calendarId=CALENDAR_ID, eventId=instance['id']).execute()
        #     print(instance['id'])

if __name__ == "__main__":
    creds = authEvent()
    eventIds = readEvent(creds)
    deleteEvent(creds, eventIds)
