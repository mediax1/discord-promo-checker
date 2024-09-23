import requests
import threading
import random
import os
import time
import logging
import json
import re
from colorama import Fore, Style, init
from datetime import datetime, timezone
from dateutil import parser
from concurrent.futures import ThreadPoolExecutor, as_completed


init(autoreset=True)

ASCII_ART = r"""
 ____             _    _____
|  _ \  __ _ _ __| | _| ____|   _  ___  ___ 
| | | |/ _` | '__| |/ /  _|| | | |/ _ \/ __|
| |_| | (_| | |  |   <| |__| |_| |  __/\__ \
|____/ \__,_|_|  |_|\_\_____\__, |\___||___/
                            |___/  
                                  by @mediax1 | discord.gg/darkeyes
"""

PROXY_FAILURE_THRESHOLD = 3
proxy_failures = {}

def create_output_directory():
    if not os.path.exists("output"):
        os.makedirs("output")

def setup_logging():
    logging.basicConfig(
        filename='output/checker.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def load_config(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"The file '{filename}' was not found.")
        return {}

def load_proxies(filename):
    try:
        with open(filename, "r") as f:
            proxies = [line.strip() for line in f.readlines()]
            invalid_proxies = [proxy for proxy in proxies if not is_valid_proxy(proxy)]
            if invalid_proxies:
                print(f"{Fore.RED}Invalid proxies detected! The following proxies are not in the correct format: {invalid_proxies}")
                return []
            return proxies
    except FileNotFoundError:
        logging.error(f"The file '{filename}' was not found.")
        return []


def mark_proxy_as_failed(proxy):
    proxy_failures[proxy] = proxy_failures.get(proxy, 0) + 1
    if proxy_failures[proxy] >= PROXY_FAILURE_THRESHOLD:
        print(f"{Fore.RED}Marking proxy as unhealthy: {proxy}{Style.RESET_ALL}")
        logging.warning(f"Proxy marked unhealthy: {proxy}")

def get_healthy_proxies(proxies):
    if proxies is None:
        return []
    return [proxy for proxy in proxies if proxy_failures.get(proxy, 0) < PROXY_FAILURE_THRESHOLD]

def is_valid_proxy(proxy):
    pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+:[\w]+:[\w]+$"
    return re.match(pattern, proxy) is not None

def load_promos(filename):
    try:
        with open(filename, "r") as f:
            promos = [line.strip() for line in f.readlines()]
            if not promos:
                print(f"{Fore.RED}Error: The promo file '{filename}' is empty.{Style.RESET_ALL}")
                return None
            
            unique_promos = list(set(promos))
            if len(unique_promos) < len(promos):
                print(f"{Fore.YELLOW}Warning: Duplicate promos found and removed.{Style.RESET_ALL}")
                with open(filename, "w") as f:
                    for promo in unique_promos:
                        f.write(promo + "\n")

            return unique_promos
    except FileNotFoundError:
        logging.error(f"The file '{filename}' was not found.")
        return None

def write_to_file(filename, message, plain_text=False):

    if plain_text:
        message = message.replace(Fore.GREEN, "").replace(Fore.RED, "").replace(Fore.LIGHTBLUE_EX, "")
        message = message.replace(Fore.YELLOW, "").replace(Style.RESET_ALL, "").replace(Style.BRIGHT, "")
        message = message.replace(Fore.CYAN, "").replace(Fore.MAGENTA, "").replace(Fore.LIGHTCYAN_EX, "")
    
    with open(filename, "a") as f:
        f.write(message + "\n")

def extract_promo_code(promo_url):
    return promo_url.split("/")[-1] 

def check_promo(promo, proxies, summary):
    start_time = time.time() 
    
    url = f"https://discord.com/api/v9/entitlements/gift-codes/{promo}?with_application=false&with_subscription_plan=true"
    
    healthy_proxies = get_healthy_proxies(proxies)
    proxy = random.choice(healthy_proxies) if healthy_proxies else None

    if proxy:
        ip, port, user, pw = proxy.split(":")
        proxy_string = f"http://{user}:{pw}@{ip}:{port}"
        proxies_dict = {
            "http": proxy_string,
            "https": proxy_string
        }
    else:
        proxies_dict = None

    try:
        response = requests.get(url, proxies=proxies_dict, timeout=10)
        end_time = time.time() 
        elapsed_time = end_time - start_time 
        
        if response.status_code == 200:
            r_json = response.json()
            logging.info(f"Response for promo {promo}: {r_json}")
            
            uses = r_json.get('uses', 0)
            max_uses = r_json.get('max_uses', 1)
            redeemed = r_json.get('redeemed', False)

            expires_at = r_json.get('expires_at')
            if expires_at:
                expires_date = parser.isoparse(expires_at)
                current_utc_time = datetime.now(timezone.utc)
                days_left = (expires_date - current_utc_time).days
            else:
                days_left = "Unknown"

            if uses == 0 and not redeemed:
                message = f"{Fore.GREEN}Unclaimed Promo: {Fore.LIGHTBLUE_EX}https://promos.discord.gg/{promo} | Days Left: {days_left} | Time: {elapsed_time:.2f}s{Style.RESET_ALL}"
                print(message)
                write_to_file("output/unclaimed_promos.txt", f"https://promos.discord.gg/{promo}", plain_text=True)
                summary['unclaimed'] += 1
            elif uses >= 1 and max_uses == 1:
                message = f"{Fore.RED}Claimed Promo: {Fore.LIGHTBLUE_EX}https://promos.discord.gg/{promo} | Time: {elapsed_time:.2f}s{Style.RESET_ALL}"
                print(message)
                write_to_file("output/claimed_promos.txt", f"https://promos.discord.gg/{promo}", plain_text=True)
                summary['claimed'] += 1
            else:
                message = f"{Fore.YELLOW}Promo status unclear for: {Fore.LIGHTBLUE_EX}https://promos.discord.gg/{promo} | Time: {elapsed_time:.2f}s{Style.RESET_ALL}"
                print(message)
                write_to_file("output/error_checking_promos.txt", f"https://promos.discord.gg/{promo}", plain_text=True)

        elif response.status_code == 404:
            message = f"{Fore.RED}Invalid Promo: {Fore.LIGHTBLUE_EX}https://promos.discord.gg/{promo} | Time: {elapsed_time:.2f}s{Style.RESET_ALL}"
            print(message)
            write_to_file("output/invalid_promos.txt", f"https://promos.discord.gg/{promo}", plain_text=True)
            summary['invalid'] += 1 
        elif response.status_code == 429:
            logging.warning(f"Rate limit exceeded for promo: {promo}. Retrying after delay.")
            print(f"{Fore.YELLOW}Rate limit exceeded for promo: {promo}. Retrying after delay...{Style.RESET_ALL}")
            time.sleep(10)
            mark_proxy_as_failed(proxy)
            check_promo(promo, proxies, summary)
        else:
            message = f"{Fore.RED}Error checking promo: {promo} (Status Code: {response.status_code}) | Time: {elapsed_time:.2f}s{Style.RESET_ALL}"
            print(message)
            write_to_file("output/error_checking_promos.txt", f"https://promos.discord.gg/{promo}", plain_text=True)

    except requests.exceptions.RequestException as e:
        end_time = time.time() 
        elapsed_time = end_time - start_time
        message = f"{Fore.RED}An error occurred while checking promo {promo}: {e} | Time: {elapsed_time:.2f}s{Style.RESET_ALL}"
        print(message)
        write_to_file("output/error_checking_promos.txt", f"https://promos.discord.gg/{promo}", plain_text=True)
        mark_proxy_as_failed(proxy)


def main():
    print(Style.BRIGHT + Fore.MAGENTA + ASCII_ART + Style.RESET_ALL)
    create_output_directory()
    setup_logging()
    config = load_config("config.json")
    promos = load_promos(config.get("promos_file", "promos.txt"))

    if promos is None:
        print("Exiting the program due to empty promo file.")
        return

    proxies = load_proxies(config.get("proxies_file", "proxies.txt"))

    if not proxies:
        user_input = input(f"{Fore.YELLOW}No valid proxies found. Do you want to continue in proxyless mode? (y/n): {Style.RESET_ALL}").strip().lower()
        if user_input != 'y':
            print(f"{Fore.RED}Exiting the program.{Style.RESET_ALL}")
            return
        proxies = None

    user_input = input(f"{Fore.CYAN}Start checking promos? Type 'y' to continue or 'n' to exit: ").strip().lower()
    if user_input != 'y':
        print(f"{Fore.YELLOW}Exiting the program.{Style.RESET_ALL}")
        return

    summary = {
        'claimed': 0,
        'unclaimed': 0,
        'invalid': 0
    }

    num_threads = config.get("num_threads", 20)

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(check_promo, extract_promo_code(promo_url), proxies, summary) for promo_url in promos]
        for future in as_completed(futures):
            future.result() 

    print(Style.BRIGHT + Fore.CYAN + "\nSummary of Promo Checks:" + Style.RESET_ALL)
    print(f"{Fore.GREEN}Unclaimed Promos: {summary['unclaimed']}{Style.RESET_ALL}")
    print(f"{Fore.RED}Claimed Promos: {summary['claimed']}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Invalid Promos: {summary['invalid']}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()