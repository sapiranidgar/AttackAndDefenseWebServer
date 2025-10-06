import requests

from server.server_requests.all_ips_in_country_request import AllIPsInCountryRequest
from server.server_requests.country_request import CountryRequest
from server.server_requests.server_request import ServerRequest
from web_attacks.attack_controller import AttackController
from web_attacks.attack_parameters import AttackParameters
from web_attacks.attack_type import AttackType

SERVER_URL = "http://127.0.0.1:8000"
GET_COUNTRY_OF_ADDRESS_URL = "/get_country"
GET_ALL_IPS_URL = "/get_all_ip_in_country"
GET_TOP_COUNTRIES_URL = "/get_top_countries"


class Client:
    def __init__(self):
        self.__attack_controller = AttackController.get_instance()

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
        attack_parameters = AttackParameters(target_ip=target_address, target_port=target_port,
                                             num_of_requests=number_of_packets)
        attack_type = AttackType.SYN_FLOOD_DIRECT
        self.__attack_controller.perform_attack(attack_parameters, attack_type)

    def perform_syn_flood_spoofed_attack(self, target_address: str, target_port: int, number_of_packets: int):
        attack_parameters = AttackParameters(target_ip=target_address, target_port=target_port,
                                             num_of_requests=number_of_packets)
        attack_type = AttackType.SYN_FLOOD_SPOOFED
        self.__attack_controller.perform_attack(attack_parameters, attack_type)

    def perform_url_brute_force_attack(self, target_url: str, number_of_packets: int):
        attack_parameters = AttackParameters(target_ip=target_url,
                                             num_of_requests=number_of_packets)
        attack_type = AttackType.URL_BRUTE_FORCE
        self.__attack_controller.perform_attack(attack_parameters, attack_type)

    def perform_icmp_smurf_attack(self, target_address: str, number_of_packets: int):
        attack_parameters = AttackParameters(target_ip=target_address,
                                             num_of_requests=number_of_packets)
        attack_type = AttackType.ICMP_SMURF
        self.__attack_controller.perform_attack(attack_parameters, attack_type)

    def get_attack_details(self, attack_type: AttackType) -> str:
        return self.__attack_controller.get_attack_details(attack_type)