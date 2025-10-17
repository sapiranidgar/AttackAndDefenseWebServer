import time
from collections import defaultdict
from scapy.layers.inet import IP, ICMP
from proxy.attack_detections.attack_detector import AttackDetector
import threading

ICMP_COUNT_LIMIT = 50
ICMP_TIME_WINDOW = 20
ECHO_TYPE_REQUEST = 8

class ICMPSmurfAttackDetector(AttackDetector):
    def __init__(self, count_limit: int = ICMP_COUNT_LIMIT, time_window: int = ICMP_TIME_WINDOW):
        self.__icmp_counts = defaultdict(list)
        self.__count_limit = count_limit
        self.__time_window = time_window
        self.__lock = threading.Lock()

    def analyze_single_packet(self, pkt):
        if IP in pkt and ICMP in pkt:
            icmp_type = pkt[ICMP].type

            if icmp_type == ECHO_TYPE_REQUEST: # only count echo requests (type 8)
                src = pkt[IP].src
                now = time.time()
                with self.__lock:
                    self.__icmp_counts.setdefault(src, []).append(now)
                    self.__icmp_counts[src] = [t for t in self.__icmp_counts[src] if
                                                now - t < self.__time_window]

    def get_ips_to_block(self) -> list[tuple[str, str]]:
        ips_to_block = []
        with self.__lock:
            for src, history in list(self.__icmp_counts.items()):
                if len(history) > self.__count_limit:
                    ips_to_block.append((src, f"ICMP Smurf detected: {len(history)} ICMP requests in {self.__time_window}s"))
        return ips_to_block

    def reset_detector(self):
        with self.__lock:
            self.__icmp_counts = {}
