import requests
from bs4 import BeautifulSoup
from config.redisClient import redisClient
from redis.exceptions import RedisError


import json
import re

from data_provider.mawaqit_provider import MawaqitProvider
from exceptions.scraping_exception import ScrapingException
from models.types import MawaqitYearCalendar


class ScrapingMawaqitProvider(MawaqitProvider):

    def __init__(self, masjid_url_or_endpoint: str):
        super().__init__()
        if masjid_url_or_endpoint.startswith("http"):
            self.masjid_url = masjid_url_or_endpoint
            self.masjid_endpoint = self.masjid_url.split("/")[-1]
        else:
            self.masjid_endpoint = masjid_url_or_endpoint
            self.masjid_url = f"https://mawaqit.net/en/{self.masjid_endpoint}"

    @staticmethod
    def _fetch_mawaqit(masjid_url:str):
        WEEK_IN_SECONDS = 604800
        retrieved_data = None

        # Check if Redis client is initialized
        if redisClient is not None:
            try:
                retrieved_data = redisClient.get(masjid_url)
            except RedisError:
                print("Error when reading from cache")

            if retrieved_data:
                return json.loads(retrieved_data)

        r = requests.get(masjid_url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            script = soup.find('script', string=re.compile(r'var confData = (.*?);', re.DOTALL))
            if script:
                mawaqit = re.search(r'var confData = (.*?);', script.string, re.DOTALL)
                if mawaqit:
                    conf_data_json = mawaqit.group(1)
                    conf_data = json.loads(conf_data_json)
                    # Store data in Redis if client is initialized
                    if redisClient is not None:
                        redisClient.set(masjid_url, json.dumps(conf_data), ex=WEEK_IN_SECONDS)
                    return conf_data
                else:
                    raise ScrapingException(f"Failed to extract confData JSON for {masjid_url}")
            else:
                print("Script containing confData not found.")
                raise ScrapingException(f"Script containing confData not found for {masjid_url}")
        if r.status_code == 404:
            raise ScrapingException(f"{masjid_url} not found")

    @staticmethod
    def _get_calendar(masjid_url:str):
        confData = ScrapingMawaqitProvider._fetch_mawaqit(masjid_url)
        return confData["calendar"]

    def getCurrentYearCalendar(self) -> MawaqitYearCalendar:
        return ScrapingMawaqitProvider._get_calendar(self.masjid_url)
