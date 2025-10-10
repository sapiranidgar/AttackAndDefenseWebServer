import logging
import threading

import pytz
from datetime import datetime
from typing import Optional

from common_objects.responses import Response, DataResponse
from common_utils import is_valid_ip_address
from server.server_executor import Server
from server.server_requests.all_ips_in_country_request import AllIPsInCountryRequest
from server.server_requests.country_request import CountryRequest

logger = logging.getLogger(__name__)
utc = pytz.UTC

DEFAULT_NUMBER_OF_COUNTRIES = 5


class ServerController:
    __server = Server()
    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        raise RuntimeError("This is a Singleton. Invoke get_instance() instead.")

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super().__new__(cls)

        return cls.__instance

    def get_country(self, request: CountryRequest) -> Response[str]:
        try:
            ip_address = request.ip_address
            if self.__valid_ip_address(ip_address):
                country = self.__server.get_geolocation_by_address(ip_address, datetime.now())
                if country is None or country == "":
                    logger.warning("Could not find the country for the given IP address in the geolocation request.")
                    return Response(error_msg="Failed to retrieve the ip's country", status_code=500)
                return DataResponse(country)
            else:
                logger.warning("User sent invalid ip address for geolocation request.")
                return Response(error_msg="Invalid IP address.", status_code=400)
        except Exception as e:
            return Response(error_msg=str(e), status_code=500)

    @classmethod
    def __valid_ip_address(cls, ip_address: str) -> bool:
        return is_valid_ip_address(ip_address)

    def get_all_ips(self, request: AllIPsInCountryRequest) -> Response[list[str]]:
        country = request.country
        start_time = request.start_date
        end_time = request.end_date
        try:
            if not self.__valid_country(country):
                logger.warning("User sent invalid country for all addresses request. It doesn't appear in the DB.")
                return Response(error_msg="Invalid country or country has 0 requests.", status_code=400)

            if not self.__valid_date_filters(start_time, end_time):
                logger.warning("User sent invalid time filters for all addresses request.")
                return Response(error_msg="Invalid filtering dates.", status_code=400)

            ip_addresses = self.__server.get_all_ips_of_country(country, start_time, end_time)
            return DataResponse(ip_addresses)
        except Exception as e:
            return Response(error_msg=str(e), status_code=500)

    def __valid_country(self, country: str) -> bool:
        return country in self.__server.get_all_available_countries()

    def __valid_date_filters(self, start_time: Optional[datetime], end_time: Optional[datetime]) -> bool:
        if start_time is None and end_time is None:
            return True
        if start_time is not None and end_time is not None and start_time > end_time:
            return False
        if start_time is not None and start_time > utc.localize(datetime.now()):
            return False
        return True

    def get_top_countries(self) -> Response[list[str]]:
        try:
            top_countries = self.__server.get_top_countries(DEFAULT_NUMBER_OF_COUNTRIES)
            return DataResponse(top_countries)
        except Exception as e:
            return Response(error_msg=str(e), status_code=500)
