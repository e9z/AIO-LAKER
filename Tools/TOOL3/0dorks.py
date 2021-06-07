
import requests
import os
import datetime
from colorama import Fore, Style
from bs4 import BeautifulSoup
from threading import Thread
from queue import Queue
import random
import time
from urllib.parse import urlparse
from engines import ProxiesEngine

# Queue declaration
dork_queue = Queue()

# Default threads number
THREADS_TO_USE = 10

# Here you can change the result filename
RESULT_FILE = '0dorkresults-' + str(datetime.datetime.now()).replace(' ', '').replace(':', '') + '.txt'

# You can add more domain extensions here to increase the search results
DOMAINS_EXTENSION = [
    "com",
    "net",
    "org",
    "co",
    "mx",
    "com.mx",
    "ar"
]

def producer(dorks):
    for dork in dorks:
        new_dork = dork.replace("\n", "")
        dork_queue.put(new_dork)

def consumer(with_full_path, proxy_manager):
    while True:
        dork = dork_queue.get()
        try:
            print(f'[{Fore.YELLOW}TARGET{Style.RESET_ALL}] {dork}')
            bing_search(dork, with_full_path, proxy_manager)
            # google_search(dork, with_full_path, proxy_manager)
        except:
            pass
        dork_queue.task_done()


def remove_duplicates():
    """
    Remove file duplicates
    """
    file_target = input(f"{Fore.LIGHTCYAN_EX}Target file << {Style.RESET_ALL}")
    if file_target and os.path.exists(file_target):
        with open(file_target, 'r') as target_file:
            content = list(set(target_file))
            with open('without-duplicates.txt', 'a') as wd:
                for line in content:
                    wd.write(line)

def bing_search(query, full_path, proxy_manager):
    """
    Search on bing engine
    """
    for extension in DOMAINS_EXTENSION:
        # proxy selection
        proxies = {}
        if proxy_manager:
            proxy = proxy_manager.select_one().with_format()
            proxies = {'http': proxy}
            print(f"{Fore.LIGHTCYAN_EX}[ PROXY ]{Style.RESET_ALL} {proxy}")
        start = 0
        print(f"{Fore.LIGHTCYAN_EX}[ Searching Bing ]{Style.RESET_ALL} {query} site:{extension}")
        for x in range(0, 5):
            sleep_time = random.randint(1, 4)
            time.sleep(sleep_time)
            response = requests.get(f'https://www.bing.com/search?count=50&q={query} site:{extension}&offset={start}', headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
            }, proxies=proxies)
            if response.status_code == 200:
                start += 50
                soup = BeautifulSoup(response.text, 'html.parser')
                containers = soup.find_all('li', {'class': 'b_algo'})
                for container in containers:
                    link = container.find('a').get('href')
                    if not full_path:
                        link = urlparse(link).netloc
                    save_result(link)
                    print(f'{Fore.GREEN} [URL BING] {link} {Style.RESET_ALL}')


def google_search(query, full_path, proxy_manager):
    """
    Google request.
    """
    for extension in DOMAINS_EXTENSION:
        # Proxy selection
        proxies = {}
        if proxy_manager:
            proxy = proxy_manager.select_one().with_format()
            proxies = {'http': proxy}
            print(f"{Fore.LIGHTCYAN_EX}[ PROXY ]{Style.RESET_ALL} {proxy}")
        start = 0
        print(f"{Fore.LIGHTCYAN_EX}[ Searching Google ]{Style.RESET_ALL} {query} site:{extension}")
        for x in range(0, 4):
            sleep_time = random.randint(3, 7)
            time.sleep(sleep_time)
            response = requests.get(f'https://www.google.com/search?num=50&q={query} site:{extension}&start={start}', headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
            }, proxies=proxies)
            if response.status_code == 200:
                start += 100
                soup = BeautifulSoup(response.text, 'html.parser')
                containers = soup.find_all('div', {'class': 'g'})
                for container in containers:
                    link = container.find('a').get('href')
                    if not full_path:
                            link = urlparse(link).netloc
                    save_result(link)
                    print(f'{Fore.GREEN} [URL GOOGLE] {link} {Style.RESET_ALL}')

def save_result(line):
    """
    Save the result on the target file
    """
    with open(RESULT_FILE, 'a') as result_file:
        result_file.write(f"{line}\n")


def single_dork_search():
    """
    This function make a single dork search
    """
    # Getting the dork
    dork_line = input(f"{Fore.LIGHTBLUE_EX} Dork line (Ej. inurl:index.php) << {Style.RESET_ALL} ")

    # Getting the path configuration
    fullpath = False
    useFullPath = input(f"{Fore.LIGHTBLUE_EX} Do you whant the full path (y/n) (default: n) << {Style.RESET_ALL} ")
    if useFullPath == 'y':
        fullpath = True
    
    # Getting the proxy configuration
    proxies = input(f"{Fore.LIGHTBLUE_EX} Proxy file ? (Ej. c:/proxies.txt) << {Style.RESET_ALL} ")
    proxy_manager = None
    if proxies and os.path.exists(proxies):
        proxy_manager = ProxiesEngine(proxies)

    if dork_line:
        google_search(dork_line, fullpath, proxy_manager)
        bing_search(dork_line, fullpath, proxy_manager)
    else:
        print(f"{Fore.RED}Not dork was supplied{Style.RESET_ALL}")

def dork_file_search():
    """
    This function defines the search using a dorkfiel
    """
    # Getting the dork
    dork_file = input(f"{Fore.LIGHTBLUE_EX} Dork file path (Ej. c:/dorks.txt) << {Style.RESET_ALL} ")
    fullpath = False
    
    # Getting the path configuration
    useFullPath = input(f"{Fore.LIGHTBLUE_EX} Do you whant the full path (y/n) (default: n) << {Style.RESET_ALL} ")
    if useFullPath == 'y':
        fullpath = True

    # Getting the proxy configuration
    proxies = input(f"{Fore.LIGHTBLUE_EX} Proxy file ? (Ej. c:/proxies.txt) << {Style.RESET_ALL} ")
    proxy_manager = None
    if proxies and os.path.exists(proxies):
        proxy_manager = ProxiesEngine(proxies)

    if dork_file and os.path.exists(dork_file):
        with open(dork_file, 'r') as dorks:
            lines = dorks.readlines()
            for x in range(THREADS_TO_USE):
                job = Thread(target=consumer, args=(fullpath, proxy_manager,))
                job.daemon = True
                job.start()
            producer(lines)
            dork_queue.join()

    else:
        print(f"{Fore.RED}Not dork file was supplied{Style.RESET_ALL}")

if __name__ == "__main__":
    """
    Script entrypoint
    """
    print(f"""{Fore.CYAN}
            

 ██████╗ ██╗  ██╗██████╗  ██████╗ ██████╗ ██╗  ██╗    
██╔═████╗╚██╗██╔╝██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝    
██║██╔██║ ╚███╔╝ ██║  ██║██║   ██║██████╔╝█████╔╝     
████╔╝██║ ██╔██╗ ██║  ██║██║   ██║██╔══██╗██╔═██╗     
╚██████╔╝██╔╝ ██╗██████╔╝╚██████╔╝██║  ██║██║  ██╗    
 ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    
                                                      
             
        {Style.RESET_ALL}

        {Fore.GREEN} 0xDork By LAKER {Style.RESET_ALL}

        {Fore.YELLOW} INSTA: {Style.RESET_ALL} @E9_z_
        {Fore.YELLOW} TELEGRAM :  {Style.RESET_ALL} LAKER305
    """)

    print(f"""
        {Fore.YELLOW}[ 1 ]{Style.RESET_ALL} Single dork search
        {Fore.YELLOW}[ 2 ]{Style.RESET_ALL} Dork file search
        {Fore.YELLOW}[ 3 ]{Style.RESET_ALL} Remove duplicates
    """)

    option = input(f"Select an option << ")

    if option == '1':
        single_dork_search()
    elif option == '2':
        dork_file_search()
    elif option == '3':
        remove_duplicates()
    else:
        print(f"{Fore.RED}Not valid option selected{Style.RESET_ALL}")


