from mawaqit_api.scraping import script as api

from data_provider.mawaqit_provider import MawaqitProvider
from models.types import MawaqitYearCalendar


class ApiMawaqitProvider(MawaqitProvider):

    def __init__(self, masjid_url_or_endpoint: str):
        super().__init__()
        if masjid_url_or_endpoint.startswith("http"):
            self.masjid_url = masjid_url_or_endpoint
            self.masjid_endpoint = self.masjid_url.split("/")[-1]
        else:
            self.masjid_endpoint = masjid_url_or_endpoint
            self.masjid_url = f"https://mawaqit.net/en/{self.masjid_endpoint}"

    def getCurrentYearCalendar(self) -> MawaqitYearCalendar:
        return api.get_calendar(self.masjid_endpoint)
