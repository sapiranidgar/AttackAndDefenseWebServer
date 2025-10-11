import threading
import time

DEFAULT_REQUEST_LIMIT = 5
DEFAULT_PATHS_LIMIT = 5
DEFAULT_TIME_WINDOW = 10

class ProxyController:
    """
    A simple interface for monitoring and blocking potential DoS attacks.
    Extend this class to add more detection logic.
    """

    __rate_history = None
    __path_history = None
    __request_limit = None
    __path_limit = None
    __time_window = None
    __blocked_ips = None

    __instance = None
    __lock = threading.Lock()

    @classmethod
    def get_instance(cls, request_limit: int = DEFAULT_REQUEST_LIMIT, path_limit: int = DEFAULT_PATHS_LIMIT,
                     time_window: int = DEFAULT_TIME_WINDOW):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super().__new__(cls)
                    cls.__instance.__request_limit = request_limit
                    cls.__instance.__path_limit = path_limit
                    cls.__instance.__time_window = time_window
                    cls.__instance.__blocked_ips = set()
                    cls.__instance.__rate_history = {}
                    cls.__instance.__path_history = {}
        return cls.__instance

    def __is_regular_dos_attack(self, ip: str, current_timestamp: float) -> bool:
        # Track request frequency
        self.__rate_history.setdefault(ip, []).append(current_timestamp)
        self.__rate_history[ip] = [t for t in self.__rate_history[ip] if current_timestamp - t < self.__time_window]

        # check if the same ip sent more than allowed request in a single time window
        if len(self.__rate_history[ip]) > self.__request_limit:
            self.__blocked_ips.add(ip)
            print(f"[PROXY] Temporarily blocking {ip} due to flood.")
            return True

        return False

    def __is_url_bruteforce_attack(self, ip: str, current_timestamp: float, path: str) -> bool:
        # --- URL brute force detection ---
        self.__path_history.setdefault(ip, [])
        self.__path_history[ip].append((path, current_timestamp))
        self.__path_history[ip] = [(p, t) for p, t in self.__path_history[ip] if current_timestamp - t < self.__time_window]

        unique_paths = len(set(p for p, _ in self.__path_history[ip]))
        if unique_paths > self.__path_limit:
            self.block_ip(ip, reason="URL brute-force detected (too many unique paths)")
            return True

        return False

    def is_allowed(self, ip: str, path: str) -> bool:
        """Check rate limits and if IP is blocked."""
        if ip in self.__blocked_ips:
            return False
        now = time.time()
        dos_attacker = self.__is_regular_dos_attack(ip, now)
        url_brute_force_attacker = self.__is_url_bruteforce_attack(ip, now, path)

        if dos_attacker:
            self.block_ip(ip, "Excessive request rate (DoS)")
            return False
        elif url_brute_force_attacker:
            self.block_ip(ip, "Excessive paths rate (URL Bruteforce)")
            return False

        return True

    def block_ip(self, ip: str, reason: str):
        """Block an IP and log the reason."""
        if ip not in self.__blocked_ips:
            print(f"[CONTROLLER] Blocking {ip}: {reason}")
            self.__blocked_ips.add(ip)
