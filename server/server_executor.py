import logging
import json
from datetime import datetime
from typing import Optional
from urllib.request import urlopen

from server.server_db import ServerDatabase

logger = logging.getLogger(__name__)

GEOLOCATION_URL_PREFIX = "https://ipinfo.io/"
GEOLOCATION_URL_SUFFIX = "/json"

COUNTRY_KEY = "country"
BOGON_KEY = "bogon"
BOGON_IP_MESSAGE = "Bogon IP. No country available."


class Server:
    def __init__(self):
        self.__server_db = ServerDatabase()

    def get_geolocation_by_address(self, ip_address: str, start_date: datetime) -> str:
        url = GEOLOCATION_URL_PREFIX + ip_address + GEOLOCATION_URL_SUFFIX

        try:
            ip_country_response = json.load(urlopen(url))
            if COUNTRY_KEY in ip_country_response:
                ip_country = ip_country_response[COUNTRY_KEY]
            elif BOGON_KEY in ip_country_response and ip_country_response[BOGON_KEY]:
                return BOGON_IP_MESSAGE
            else:
                logger.error(f"Received wrong country response for ip address: {ip_address}.")
                return ""
        except Exception as e:
            logger.error(f"Could not load country for ip address: {ip_address}. The error is: {e}")
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
