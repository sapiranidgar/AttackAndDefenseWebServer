import time
import re
from collections import defaultdict
from scapy.layers.inet import IP, TCP
from proxy.attack_detections.attack_detector import AttackDetector
import threading

UNIQUE_PATHS_LIMIT = 20
PATH_TIME_WINDOW = 30

HTTP_METHOD_RE = re.compile(rb'^(GET|POST|PUT|DELETE|PATCH|OPTIONS|HEAD)\s+(/[^ ]*)\s+HTTP/')

class UrlBruteForceAttackDetector(AttackDetector):
    def __init__(self, unique_paths_limit: int = UNIQUE_PATHS_LIMIT, time_window: int = PATH_TIME_WINDOW):
        self.__path_history = defaultdict(list)
        self.__unique_paths_limit = unique_paths_limit
        self.__time_window = time_window
        self.__lock = threading.Lock()

    def analyze_single_packet(self, pkt):
        if not (IP in pkt and TCP in pkt):
            return

        payload = bytes(pkt[TCP].payload)
        if not payload:
            return
        http_method = HTTP_METHOD_RE.match(payload)
        if not http_method:
            return
        path_bytes = http_method.group(2)
        try:
            path = path_bytes.decode('utf-8', errors='ignore')
        except Exception:
            path = path_bytes.decode('latin-1', errors='ignore')
        src = pkt[IP].src
        now = time.time()
        with self.__lock:
            self.__path_history[src].append((path, now))

    def get_ips_to_block(self) -> list[tuple[str, str]]:
        now = time.time()
        ips_to_block = []
        with self.__lock:
            for src, entries in list(self.__path_history.items()):
                entries = [(p, t) for (p, t) in entries if now - t < self.__time_window]
                self.__path_history[src] = entries
                unique_paths = len(set(p for p, _ in entries))
                if unique_paths > self.__unique_paths_limit:
                    ips_to_block.append((src, f"URL brute-force detected: {unique_paths} unique paths in {self.__time_window}s"))
        return ips_to_block

    def reset_detector(self):
        with self.__lock:
            self.__path_history.clear()
