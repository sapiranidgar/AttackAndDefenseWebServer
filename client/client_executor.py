from typing import Optional

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

MIN_NUMBER_OF_PACKETS_FOR_ATTACK = 10


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

    def __valid_number_of_packets(self, number_of_packets: int) -> bool:
        if number_of_packets < MIN_NUMBER_OF_PACKETS_FOR_ATTACK:
            return False
        return True

    def __perform_attack(self, target_ip: str, target_port: Optional[int], num_of_requests: int,
                         attack_type: AttackType):
        if not self.__valid_number_of_packets(num_of_requests):
            raise ValueError(
                f"Number of packets for performing the attack is invalid. Try again with {MIN_NUMBER_OF_PACKETS_FOR_ATTACK} packets or more.")

        attack_parameters = AttackParameters(target_ip=target_ip, target_port=target_port,
                                             num_of_requests=num_of_requests)
        self.__attack_controller.perform_attack(attack_parameters, attack_type)

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
        self.__perform_attack(target_address, target_port, number_of_packets, AttackType.SYN_FLOOD_DIRECT)

    def perform_syn_flood_spoofed_attack(self, target_address: str, target_port: int, number_of_packets: int):
        self.__perform_attack(target_address, target_port, number_of_packets, AttackType.SYN_FLOOD_SPOOFED)

    def perform_url_brute_force_attack(self, target_url: str, number_of_packets: int):
        self.__perform_attack(target_url, None, number_of_packets, AttackType.URL_BRUTE_FORCE)

    def perform_icmp_smurf_attack(self, target_address: str, number_of_packets: int):
        self.__perform_attack(target_address, None, number_of_packets, AttackType.ICMP_SMURF)

    def get_attack_details(self, attack_type: AttackType) -> str:
        return self.__attack_controller.get_attack_details(attack_type)
