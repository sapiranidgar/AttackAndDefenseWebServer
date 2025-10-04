import logging
import json
from datetime import datetime
from typing import Optional
from urllib.request import urlopen

from server_database.server_db import ServerDatabase

logger = logging.getLogger(__name__)

GEOLOCATION_URL_PREFIX = "https://ipinfo.io/"
GEOLOCATION_URL_SUFFIX = "/json"

COUNTRY_KEY = "country"


class Server:
    def __init__(self):
        self.__server_db = ServerDatabase()

    def get_geolocation_by_address(self, ip_address: str, start_date: datetime) -> str:
        url = GEOLOCATION_URL_PREFIX + ip_address + GEOLOCATION_URL_SUFFIX

        try:
            ip_country = json.load(urlopen(url))[COUNTRY_KEY]
        except:
            logger.error("Could not load country for ip address: " + ip_address)
            return ""

        self.__server_db.insert_record(ip_country, ip_address, start_date)
        return ip_country

    def get_all_ips_of_country(self, country: str, start_time: Optional[datetime], end_time: Optional[datetime]) \
            -> list[str]:
        country_addresses = self.__server_db.get_records_by_country(country, start_time, end_time)
        return country_addresses

    def get_top_countries(self, number_of_countries: int) -> list[str]:
        top_countries = self.__server_db.get_countries_with_most_ips(number_of_countries)
        return top_countries

    def get_all_available_countries(self) -> list[str]:
        return self.__server_db.get_all_countries()
