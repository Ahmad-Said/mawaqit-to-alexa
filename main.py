import datetime
import os

from data_provider.api_mawaqit_provider import ApiMawaqitProvider
from data_provider.csv_mawaqit_provider import CsvMawaqitProvider
from util.param import Param
from services.calendar_generator import MawaqitCalendarGenerator

if __name__ == '__main__':
    # set the parameters
    Param.ALARM_BEFORE_MINUTES = 15
    Param.SUMMARY_PREFIX = ''
    # language = 'ar'
    language = 'en'

    ## set directly the url of the mawaqit online link
    data_url = 'https://mawaqit.net/fr/grande-mosquee-de-paris'

    ## or export data from mawaqit account as csv files
    # data_folder = 'data/Nantes'

    # generated parameters
    current_year = datetime.datetime.now().year

    if 'data_url' in locals():
        data_url = locals()['data_url']
        api_mawaqit_provider = ApiMawaqitProvider(data_url)
        year_calendar = api_mawaqit_provider.getCurrentYearCalendar()
        mosque_name = api_mawaqit_provider.masjid_endpoint
    elif 'data_folder' in locals():
        # get full path of the data folder
        data_folder = locals()['data_folder']
        mosque_name = data_folder.split('/')[-1]
        data_folder = os.path.join(os.getcwd(), data_folder)
        year_calendar = CsvMawaqitProvider(data_folder).getCurrentYearCalendar()
    else:
        raise Exception('You must set either data_folder or data_url')

    output_file = f'out/{mosque_name}_{current_year}.ics'
    output_file = os.path.join(os.getcwd(), output_file)

    # create the calendar
    MawaqitCalendarGenerator.create_mawaqit_calendar(
        year_calendar=year_calendar,
        year=current_year,
        output_file=output_file,
        time_zone='Europe/Paris',
        language=language
    )



