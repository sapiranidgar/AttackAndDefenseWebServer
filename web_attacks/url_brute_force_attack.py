import random
import string
import requests

SERVER_RANDOM_PATH_LENGTH = 5
DEFAULT_TIMEOUT = 3
DEFAULT_ATTACK_URLS = ["data", "key", "robots.txt", "admin", "config.php", "etc/resolv.conf", "etc/hosts", "httpd.conf"]

def generate_random_url() -> str:
    return ''.join(random.choices(string.ascii_letters, k=SERVER_RANDOM_PATH_LENGTH))


def perform_url_brute_force_attack(target_address: str, number_of_packets: int):
    random_urls = [generate_random_url() for _ in range(number_of_packets)]
    successful_requests = 0
    for idx, random_url_suffix in enumerate(random_urls + DEFAULT_ATTACK_URLS):
        try:
            random_url = f"{target_address}/{random_url_suffix}"
            print(random_url)
            requests.get(random_url, timeout=DEFAULT_TIMEOUT)
            successful_requests += 1
            print(f"Done sending {idx + 1} requests with random urls. Current url: {random_url}.")
        except Exception as e:
            print(f"An error occurred for packet {idx + 1}: {e}. Sent {successful_requests} packets. \nGoodbye.")
