from datetime import datetime
from urllib.request import urlopen
import json

import pandas as pd

GEOLOCATION_URL_PREFIX = "https://ipinfo.io/"
GEOLOCATION_URL_SUFFIX = "/json"

COUNTRY_KEY = "country"

COUNTRY_COLUMN = "country"
IP_ADDRESS_COLUMN = "ip"
DATE_COLUMN = "date"
GEO_LOCATION_REQUESTS_COLUMNS = [COUNTRY_COLUMN, IP_ADDRESS_COLUMN, DATE_COLUMN]


class Server:
    def __init__(self):
        self.__geo_location_requests = pd.DataFrame(columns=GEO_LOCATION_REQUESTS_COLUMNS)

    def get_geolocation_by_address(self, ip_address: str, start_date: datetime) -> str:
        url = GEOLOCATION_URL_PREFIX + ip_address + GEOLOCATION_URL_SUFFIX

        try:
            ip_country = json.load(urlopen(url))[COUNTRY_KEY]
        except:
            return ""

        current_ip_df = pd.DataFrame({
            COUNTRY_COLUMN: [ip_country],
            IP_ADDRESS_COLUMN: [ip_address],
            DATE_COLUMN: [start_date]
        })
        self.__geo_location_requests = pd.concat([self.__geo_location_requests, current_ip_df], ignore_index=True)
        return ip_country

    def get_all_ips_of_country(self, country: str) -> list[str]:
        country_df = self.__geo_location_requests[self.__geo_location_requests[COUNTRY_COLUMN] == country]
        return list(country_df[IP_ADDRESS_COLUMN])

    def get_top_countries(self, number_of_countries: int) -> list[str]:
        if self.__geo_location_requests.empty:
            return []

        len_per_country: pd.Series = self.__geo_location_requests.groupby(COUNTRY_COLUMN)[IP_ADDRESS_COLUMN].nunique()
        len_per_country_sorted = len_per_country.sort_values(ascending=False)
        return list(len_per_country_sorted.index)[:number_of_countries]

    def get_all_available_countries(self) -> list[str]:
        return self.__geo_location_requests[COUNTRY_COLUMN].unique().tolist()
