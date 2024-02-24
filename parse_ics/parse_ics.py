# takes a team sideline subscription URL and converts it to a team snap .csv

import vobject
import csv
import pytz
import datetime as dt
import requests as r

TIMEZONE_NAME = 'America/Los_Angeles'
TEAMSIDELINE_URL = 'http://tmsdln.com/28knr'
TEAM_NAME = 'Due Soccer Club (Maroon)'

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
    """
    takes a matchup description and returns the opponent name
    :description    : Teams Sideline matchup description
    :my_team        : my team name
    :returns        : opponent name for a given matchup
    """

    my_team = my_team.strip()
    opponent = ""
    if " vs. " in description:
        teams = description.split(" vs. ")
        if teams[0].strip() == my_team:
            opponent = teams[1].strip()
        else:
            opponent = teams[0].strip()
    return opponent


def get_home_away(description, my_team):
    """
    takes a matchup description and returns the home or away
    :description    : Teams Sideline matchup description
    :my_team        : my team name
    :returns        : home or away for a given matchup.  "h" for home, "a" for away.  "" if not found. 
    """
    home_away = ""
    my_team = my_team.strip()
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

    schedule = r.get(TEAMSIDELINE_URL).text

    # iterate through the contents
    for cal in vobject.readComponents(schedule):
        for component in cal.components():
            if component.name == "VEVENT":
                event_local_tz = convert_from_utc(utc_dt=component.dtstart.value, timezone_name=TIMEZONE_NAME)
                csv_writer.writerow([
                    event_local_tz.strftime("%m/%d/%Y"), # Date
                    event_local_tz.strftime("%I:%M %p"), # Time
                    '1:30', # duration
                    'Game', # Name
                    get_opponent(component.summary.value, TEAM_NAME), # opponent name
                    component.location.value, # location name
                    get_home_away(component.summary.value, TEAM_NAME) # home or away
                    ])
