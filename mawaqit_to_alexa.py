import csv
import os
import datetime
from icalendar import Calendar, Event, Alarm

from param import Param
from util.util import Util

# Get the current directory
current_directory = os.getcwd()

# List all files in the current directory
# files = os.listdir(current_directory)
# files are from 01.csv to 12.csv
i = 1
files = []
while i <= 12:
    # print digit with leading zero
    files.append(f'{i:02}.csv')
    i += 1

# List to store data from all CSV files
combined_data = []


# Create a new iCal calendar
cal = Calendar()


def get_prayer_event(prayer, day, time, suffix_id="", trigger_before=0, event_summary=""):
    prayer_datetime = datetime.datetime(
        Param.CURRENT_YEAR,
        current_month,
        int(day),
        int(time.split(':')[0]),
        int(time.split(':')[1])
    )
    # create event for each prayer and append it to calendar
    # Fajr
    event = Event()
    # join summary prefix and prayer name with a space if summary prefix is not empty
    event_summary = event_summary if event_summary else prayer
    event_summary = f'{Param.SUMMARY_PREFIX} {event_summary}' if Param.SUMMARY_PREFIX else event_summary
    event.add('summary', event_summary)
    event.add('dtstart', prayer_datetime)
    event.add('dtend', prayer_datetime)
    # set timezone to Europe/Paris
    event.add('tzid', 'Europe/Paris')
    # Unique identifier for the event
    event['uid'] = f'{prayer}-{Param.CURRENT_YEAR}-{current_month}-{day}-{suffix_id}'

    # Create an alarm 15 minutes before the event
    alarm = Alarm()
    alarm.add('action', 'DISPLAY')
    alarm.add('description', f'{prayer} prayer time before {trigger_before} minutes')
    alarm.add('trigger', datetime.timedelta(minutes=-trigger_before))
    event.add_component(alarm)
    return event


# Iterate over each file in the directory
for file in files:
    # Check if the file is a CSV
    if not file.endswith('.csv'):
        continue
    current_month = int(file[:2])
    # Open the CSV file
    with open(f"{Param.CSV_MAWAQIT_TIMETABLE_FOLDER}/{file}", 'r') as csv_file:
        # Create a CSV reader object
        csv_reader = csv.reader(csv_file)

        # Skip the first line
        next(csv_reader)

        # Read and append the remaining lines to the combined_data list
        for row in csv_reader:
            # Day,Fajr,Shuruk,Duhr,Asr,Maghrib,Isha
            # 1,07:34,08:54,13:15,15:09,17:30,18:46
            day = row[0]
            fajr = row[1]
            shuruk = row[2]
            duhr = row[3]
            asr = row[4]
            maghrib = row[5]
            isha = row[6]

            # skip leap day
            if current_month == 2 and day == '29' and Util.is_leap_year(Param.CURRENT_YEAR) == False:
                continue

            # # skip all day but current day
            # if int(day) != datetime.datetime.now().day or current_month != datetime.datetime.now().month:
            #     continue

            # # set isha after 3 minutes from now
            # isha_datetime = datetime.datetime.now() + datetime.timedelta(minutes=3)
            # isha = f'{isha_datetime.hour}:{isha_datetime.minute}'

            # Add the event to the calendar
            # event name main, event name secondary, event time
            prayer_day_list_zip = [
                ('Fajr','Fajr', fajr),
                ('Shuruk','Shuruk', shuruk),
                ('Duhr','Duhr', duhr),
                ('Asr','Asr', asr),
                ('Maghrib','Maghrib', maghrib),
                ('Isha','Isha', isha),
            ]
            # prayer_day_list_zip = [
            #     ('Fajr', 'حَيًّا عَلَى صَلَاةِ الفَجْر، الفَلاح', fajr),
            #     ('Shuruk', 'حَيًّا عَلَى صَلَاةِ الشُّروق، الفَلاح', shuruk),
            #     ('Duhr', 'حَيًّا عَلَى صَلَاةِ الظُّهْر، الفَلاح', duhr),
            #     ('Asr', 'حَيًّا عَلَى صَلَاةِ العَصْر، الفَلاح', asr),
            #     ('Maghrib', 'حَيًّا عَلَى صَلَاةِ المَغْرِب، الفَلاح', maghrib),
            #     ('Isha', 'حَيًّا عَلَى صَلَاةِ العِشَاء، الفَلاح', isha),
            # ]

            for prayer_main, prayer_secondary, time in prayer_day_list_zip:
                cal.add_component(get_prayer_event(prayer_main, day, time, suffix_id="main", trigger_before=Param.ALARM_BEFORE))
                cal.add_component(get_prayer_event(prayer_main, day, time, suffix_id="secondary", trigger_before=0, event_summary=prayer_secondary))


# Write the iCal calendar to a file
with open(f'{Param.CSV_MAWAQIT_TIMETABLE_FOLDER}/mawaqit_{Param.LOCATION}_{Param.CURRENT_YEAR}.ics', 'wb') as f:
    f.write(cal.to_ical())

