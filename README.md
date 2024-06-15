# McGill Calendar Sync

Python script that parses the student course calendar from Minerva (student portal for McGill University) and adds events to your Google Calendar.
It can also delete all the events in the school year (between August and April).

## Installation
Install the required Python packages.
``pip install -r requirements.txt``

Follow the instructions to set up the Google Calendar API connection: https://developers.google.com/calendar/api/quickstart/python

## Usage

### Syncing
Run in the terminal:
``python3 sync.py CALENDAR_ID``
and replace CALENDAR_ID with the calendar you want to add the events to.

Enter your student ID and PIN for the Guest account on Minerva (should be the one given to you during admissions).

### Deleting events
Run in the terminal:
``python3 delete.py CALENDAR_ID``
and replace CALENDAR_ID with the calendar you want to add the events to.

You may need to manually change the school year in the *delete.py* folder, with the *timeMin* and *timeMax* parameters inside the *readEvent* function.

## Credits
- I was able to authenticate to Minerva by following: https://github.com/minervaclient/minervaclient/tree/master
