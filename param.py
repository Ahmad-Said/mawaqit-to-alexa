import datetime


class Param:
    LOCATION = "Nantes"
    CSV_MAWAQIT_TIMETABLE_FOLDER = f'data/{LOCATION}'
    CURRENT_YEAR = datetime.datetime.now().year
    ALARM_BEFORE = 15  # minutes
    SUMMARY_PREFIX = ''
