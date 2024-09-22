import requests
import threading
import random
import os
import time
import logging
import json
from colorama import Fore, Style, init

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
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        logging.error(f"The file '{filename}' was not found.")
        return []

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
    """
    Writes a message to a file. If plain_text is True, color codes are stripped for file output.
    """
    if plain_text:
        message = message.replace(Fore.GREEN, "").replace(Fore.RED, "").replace(Fore.LIGHTBLUE_EX, "")
        message = message.replace(Fore.YELLOW, "").replace(Style.RESET_ALL, "").replace(Style.BRIGHT, "")
        message = message.replace(Fore.CYAN, "").replace(Fore.MAGENTA, "").replace(Fore.LIGHTCYAN_EX, "")
    
    with open(filename, "a") as f:
        f.write(message + "\n")

def extract_promo_code(promo_url):
    return promo_url.split("/")[-1]

def check_promo(promo, proxies, summary):
    url = f"https://discord.com/api/v9/entitlements/gift-codes/{promo}?with_application=false&with_subscription_plan=true"
    
    proxy = random.choice(proxies) if proxies else None
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
        
        if response.status_code == 200:
            r_json = response.json()
            logging.info(f"Response for promo {promo}: {r_json}")
            
            uses = r_json.get('uses', 0)
            max_uses = r_json.get('max_uses', 1)
            redeemed = r_json.get('redeemed', False)

            if uses == 0 and not redeemed:
                message = f"{Fore.GREEN}Unclaimed Promo: {Fore.LIGHTBLUE_EX}https://promos.discord.gg/{promo}{Style.RESET_ALL}"
                print(message)
                write_to_file("output/unclaimed_promos.txt", f"https://promos.discord.gg/{promo}", plain_text=True)
            elif uses >= 1 and max_uses == 1:
                message = f"{Fore.RED}Claimed Promo: {Fore.LIGHTBLUE_EX}https://promos.discord.gg/{promo}{Style.RESET_ALL}"
                print(message)
                write_to_file("output/claimed_promos.txt", f"https://promos.discord.gg/{promo}", plain_text=True)
            else:
                message = f"{Fore.YELLOW}Promo status unclear for: {Fore.LIGHTBLUE_EX}https://promos.discord.gg/{promo}{Style.RESET_ALL}"
                print(message)
                write_to_file("output/error_checking_promos.txt", f"https://promos.discord.gg/{promo}", plain_text=True)


        elif response.status_code == 404:
            message = f"{Fore.RED}Invalid Promo: {Fore.LIGHTBLUE_EX}https://promos.discord.gg/{promo}{Style.RESET_ALL}"
            print(message)
            write_to_file("output/invalid_promos.txt", f"https://promos.discord.gg/{promo}", plain_text=True)
            summary['invalid'] += 1
        elif response.status_code == 429:
            logging.warning(f"Rate limit exceeded for promo: {promo}. Retrying after delay.")
            print(f"{Fore.YELLOW}Rate limit exceeded for promo: {promo}. Retrying after delay...{Style.RESET_ALL}")
            time.sleep(10)
            check_promo(promo, proxies, summary)
        else:
            message = f"{Fore.RED}Error checking promo: {promo} (Status Code: {response.status_code}){Style.RESET_ALL}"
            print(message)
            write_to_file("output/error_checking_promos.txt", f"https://promos.discord.gg/{promo}", plain_text=True)

    except requests.exceptions.RequestException as e:
        message = f"{Fore.RED}An error occurred while checking promo {promo}: {e}{Style.RESET_ALL}"
        print(message)
        write_to_file("output/error_checking_promos.txt", f"https://promos.discord.gg/{promo}", plain_text=True)


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
    num_threads = config.get("num_threads", 5)

    if not proxies:
        print(f"{Fore.YELLOW}Warning: No proxies found. Running in proxyless mode.{Style.RESET_ALL}")
        user_input = input("Do you want to continue without proxies? (y/n): ").strip().lower()
        if user_input != 'y':
            print("Exiting the program.")
            return

    summary = {
        'claimed': 0,
        'unclaimed': 0,
        'invalid': 0
    }

    threads = []
    for promo_url in promos:
        promo = extract_promo_code(promo_url)
        while len(threads) >= num_threads:
            for thread in threads:
                thread.join(timeout=0.1)
            threads = [t for t in threads if t.is_alive()]

        thread = threading.Thread(target=check_promo, args=(promo, proxies, summary))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(Style.BRIGHT + Fore.CYAN + "\nSummary of Promo Checks:" + Style.RESET_ALL)
    print(f"{Fore.GREEN}Unclaimed Promos: {summary['unclaimed']}{Style.RESET_ALL}")
    print(f"{Fore.RED}Claimed Promos: {summary['claimed']}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Invalid Promos: {summary['invalid']}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()