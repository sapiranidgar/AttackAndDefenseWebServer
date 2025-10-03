import heapq
from urllib.request import urlopen
import json

GEOLOCATION_URL_PREFIX = "https://ipinfo.io/"
GEOLOCATION_URL_SUFFIX = "/json"

COUNTRY_KEY = "country"


class Server:
    def __init__(self):
        self.__all_geo_location_requests: dict[str, list[str]] = {}

    def get_geolocation_by_address(self, ip_address: str) -> str:
        url = GEOLOCATION_URL_PREFIX + ip_address + GEOLOCATION_URL_SUFFIX

        try:
            ip_country = json.load(urlopen(url))[COUNTRY_KEY]
        except:
            return ""

        if ip_country not in self.__all_geo_location_requests:
            self.__all_geo_location_requests[ip_country] = [ip_address]
        else:
            self.__all_geo_location_requests[ip_country].append(ip_address)
        return ip_country

    def get_all_ips_of_country(self, country: str) -> list[str]:
        return self.__all_geo_location_requests.get(country, [])

    def get_top_countries(self, number_of_countries: int) -> list[str]:
        if self.__all_geo_location_requests == {}:
            return []
        len_per_country = {country: len(addresses) for country, addresses in self.__all_geo_location_requests.items()}
        top_countries = heapq.nlargest(number_of_countries, len_per_country.items(), key=lambda i: i[1])
        return [country_addresses[0] for country_addresses in top_countries]


    def get_all_available_countries(self) -> list[str]:
        return list(self.__all_geo_location_requests.keys())