import socket
import requests

from server.server_requests.all_ips_in_country_request import AllIPsInCountryRequest
from server.server_requests.country_request import CountryRequest
from server.server_requests.server_request import ServerRequest
from web_attacks.syn_flood_attack import perform_syn_flood_direct_attack, perform_syn_flood_spoofed_attack

SERVER_URL = "http://127.0.0.1:8000"
GET_COUNTRY_OF_ADDRESS_URL = "/get_country"
GET_ALL_IPS_URL = "/get_all_ip_in_country"
GET_TOP_COUNTRIES_URL = "/get_top_countries"


class Client:
    def __send_post_request(self, url: str, request: ServerRequest) -> str:
        data = request.model_dump_json()
        response = requests.post(url, data=data)
        return response.content.decode("utf-8")

    def __send_get_request(self, url: str) -> str:
        response = requests.get(url)
        return response.content.decode("utf-8")

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

    def perform_syn_flood_direct_attack(self, target_address: str, target_port: int, number_of_packets: int):
        client_ip_address = socket.gethostbyname(socket.gethostname())
        perform_syn_flood_direct_attack(target_address, target_port, number_of_packets, client_ip_address)

    def perform_syn_flood_spoofed_attack(self, target_address: str, target_port: int, number_of_packets: int):
        perform_syn_flood_spoofed_attack(target_address, target_port, number_of_packets)

    def perform_url_brute_force_attack(self, target_address: str, target_port: int):
        pass

    def perform_third_attack(self, target_address: str, target_port: int):
        pass
