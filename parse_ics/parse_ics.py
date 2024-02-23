# ics to csv example
# dependency: https://pypi.org/project/vobject/

import vobject
import csv
import pytz
import datetime as dt

def convert_from_utc(utc_dt, timezone_name='America/Los_Angeles'):
    """
    converts a utc datetime object to a local datetime object with the given timezone name.

    utc_dt:         the datetime object to convert.
    timezone_name:  the name of the timezone to convert to.
    returns datetime object
    """
    # Get the current time zone
    tz = pytz.timezone(timezone_name)

    # Convert the UTC datetime to the current time zone
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(tz)



    # Format the datetime as a string
    return local_dt


def get_opponent(description, my_team):
    opponent = ""
    if " vs. " in description:
        teams = description.split(" vs. ")
        if teams[0].strip() == my_team:
            opponent = teams[1].strip()
        else:
            opponent = teams[0].strip()
    return opponent


def get_home_away(description, my_team):
    home_away = ""
    if " vs. " in description:
        teams = description.split(" vs. ")
        if teams[0].strip() == my_team:
            home_away = "h"
        else:
            home_away = "a"
    return home_away


with open('teamsnap_schedule.csv', mode='w') as csv_out:
    csv_writer = csv.writer(csv_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    header_column_names = ['Date','Time','Duration (HH:MM)','Name','Opponent Name','Location Name', 'Home or Away']
    csv_writer.writerow(header_column_names)
    my_team = 'Soccer Team' # whatever is used on gssl schedule

    # read the data from the file
    data = open("Schedule.ics").read()

    # iterate through the contents
    for cal in vobject.readComponents(data):
        for component in cal.components():
            if component.name == "VEVENT":
                event_local_tz = convert_from_utc(component.dtstart.value)
                csv_writer.writerow([
                    event_local_tz.strftime("%m/%d/%Y"), # Date
                    event_local_tz.strftime("%I:%M %p"), # Time
                    '1:30', # duration
                    'Game', # Name
                    get_opponent(component.summary.value, my_team), # opponent name
                    component.location.value, # location name
                    get_home_away(component.summary.value, my_team) # home or away
                    ])