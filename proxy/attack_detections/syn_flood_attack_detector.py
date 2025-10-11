from collections import Counter
from scapy.layers.inet import IP, TCP

from proxy.attack_detections.attack_detector import AttackDetector
import threading

SYN_COUNT_FOR_SYN_FLOOD_DETECTION = 10
SYN_PER_ACK_RATIO = 3


class SynFloodAttackDetector(AttackDetector):
    def __init__(self):
        self.__syn_count = Counter()
        self.__ack_count = Counter()
        self.__lock = threading.Lock()

    def analyze_single_packet(self, pkt):
        if IP in pkt and TCP in pkt:
            src = pkt[IP].src
            with self.__lock:
                if pkt[TCP].flags.S:
                    self.__syn_count[src] += 1
                elif pkt[TCP].flags.A:
                    self.__ack_count[src] += 1

    def get_ips_to_block(self) -> list[tuple[str, str]]:
        ips_to_block = []
        with self.__lock:
            for src, syns in self.__syn_count.items():
                acks_for_source = self.__ack_count.get(src, 0)
                if syns > SYN_PER_ACK_RATIO * acks_for_source and syns > SYN_COUNT_FOR_SYN_FLOOD_DETECTION:
                    ips_to_block.append((src, "SYN Flood detected"))
        return ips_to_block

    def reset_detector(self):
        with self.__lock:
            self.__syn_count.clear()
            self.__ack_count.clear()
