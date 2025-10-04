import requests

from server.server_requests.all_ips_in_country_request import AllIPsInCountryRequest
from server.server_requests.country_request import CountryRequest
from server.server_requests.server_request import ServerRequest

SERVER_URL = "http://127.0.0.1:8000"
GET_COUNTRY_OF_ADDRESS_URL = "/get_country"
GET_ALL_IPS_URL = "/get_all_ip_in_country"
GET_TOP_COUNTRIES_URL = "/get_top_countries"


class Client:
    def __send_post_request(self, url: str, request: ServerRequest) -> str:
        data = request.model_dump_json()
        response = requests.post(url, data=data)
        return response.content

    def __send_get_request(self, url: str) -> str:
        response = requests.get(url)
        return response.content

    def send_country_request(self, ip_address: str) -> str:
        request = CountryRequest(ip_address=ip_address)
        url = SERVER_URL + GET_COUNTRY_OF_ADDRESS_URL
        return self.__send_post_request(url, request)

    def send_get_all_addresses_in_country_request(self, country: str) -> str:
        request = AllIPsInCountryRequest(country=country)
        url = SERVER_URL + GET_ALL_IPS_URL
        return self.__send_post_request(url, request)

    def send_get_top_countries_request(self) -> str:
        url = SERVER_URL + GET_TOP_COUNTRIES_URL
        return self.__send_get_request(url)

    def perform_syn_flood_attack(self):
        pass

    def perform_url_brute_force_attack(self):
        pass

    def perform_third_attack(self):
        pass
