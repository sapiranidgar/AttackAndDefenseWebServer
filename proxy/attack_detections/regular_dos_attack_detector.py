import time
from scapy.layers.inet import IP, TCP

from proxy.attack_detections.attack_detector import AttackDetector
import threading

DOS_TIME_WINDOW = 300
DOS_REQUEST_LIMIT = 1000


class RegularDosAttackDetector(AttackDetector):
    def __init__(self, request_limit: int = DOS_REQUEST_LIMIT, time_window: int = DOS_TIME_WINDOW):
        self.__rate_history = {}
        self.__time_window = time_window
        self.__request_limit = request_limit
        self.__lock = threading.Lock()

    def analyze_single_packet(self, pkt):
        if IP in pkt:
            current_timestamp = time.time()
            src = pkt[IP].src
            with self.__lock:
                self.__rate_history.setdefault(src, []).append(current_timestamp)
                self.__rate_history[src] = [t for t in self.__rate_history[src] if
                                            current_timestamp - t < self.__time_window]

    def get_ips_to_block(self) -> list[tuple[str, str]]:
        ips_to_block = []
        for ip, history in self.__rate_history.items():
            if len(history) >= self.__request_limit:
                ips_to_block.append((ip, "Detected DOS attack. Too many requests in a single window."))

        return ips_to_block

    def reset_detector(self):
        with self.__lock:
            self.__rate_history = {}
