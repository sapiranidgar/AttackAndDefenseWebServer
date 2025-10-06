import random
import string
import requests

from web_attacks.attack_parameters import AttackParameters
from web_attacks.attacks.attack import Attack

SERVER_RANDOM_PATH_LENGTH = 5
DEFAULT_TIMEOUT = 3
DEFAULT_ATTACK_URLS = ["data", "key", "robots.txt", "admin", "config.php", "etc/resolv.conf",
                       "etc/hosts", "httpd.conf", "get_top_countries"]


class UrlBruteForceAttack(Attack):
    def perform_attack(self, attack_params: AttackParameters):
        random_urls = [self.__generate_random_url() for _ in range(attack_params.num_of_requests)]
        successful_requests = 0
        for idx, random_url_suffix in enumerate(random_urls + DEFAULT_ATTACK_URLS):
            try:
                random_url = f"{attack_params.target_ip}/{random_url_suffix}"
                print(random_url)
                requests.get(random_url, timeout=DEFAULT_TIMEOUT)
                successful_requests += 1
                print(f"Done sending {idx + 1} requests with random urls. Current url: {random_url}.")
            except Exception as e:
                print(
                    f"An error occurred for packet {idx + 1}: {e}. Sent {successful_requests} packets. \nContinuing for the next request.")

    def __generate_random_url(self) -> str:
        return ''.join(random.choices(string.ascii_letters, k=SERVER_RANDOM_PATH_LENGTH))

    def get_attack_description(self) -> str:
        return """A URL brute-force attack is when an attacker systematically tries many URLs or path names on a web server (often using automated tools) to discover hidden, unlinked, or protected resources."""

    def get_attack_name(self) -> str:
        return "URL Brute Force Attack"
