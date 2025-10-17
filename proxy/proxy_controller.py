import logging
import threading

logger = logging.getLogger(__name__)

DEFAULT_REQUEST_LIMIT = 5
DEFAULT_PATHS_LIMIT = 5
DEFAULT_TIME_WINDOW = 10


class ProxyController:
    """
    A simple interface for managing DoS attackers.
    """

    __blocked_ips = set()
    __instance = None
    __lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super().__new__(cls)
        return cls.__instance

    def is_allowed(self, ip: str, path: str) -> bool:
        """Check rate limits and if IP is blocked."""
        with self.__lock:
            if ip in self.__blocked_ips:
                return False

        return True

    def block_ip(self, ip: str, reason: str):
        """Block an IP and log the reason."""
        with self.__lock:
            if ip not in self.__blocked_ips:
                logger.warning("Blocked ip: {ip}. Reason: {reason}".format(ip=ip, reason=reason))
                self.__blocked_ips.add(ip)
