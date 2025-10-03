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
        res = urlopen(url)
        data = json.load(res)
        country = data[COUNTRY_KEY]
        if country not in self.__all_geo_location_requests:
            self.__all_geo_location_requests[country] = [ip_address]
        else:
            self.__all_geo_location_requests[country].append(ip_address)
        return country
