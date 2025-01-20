import os
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs
from colorama import Fore, Style

logging.basicConfig(format='%(message)s', level=logging.INFO)
logging.getLogger('').handlers[0].setFormatter(logging.Formatter('%(message)s'))

def fetch_links_from_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        links = set()
        for a_tag in soup.find_all("a", href=True):
            full_url = urljoin(url, a_tag["href"])
            links.add(full_url)

        return list(links)
    except requests.RequestException as e:
        logging.error(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Failed to fetch links from {url}: {e}")
        return []

def filter_links(links, pattern=None):
    filtered = []
    for link in links:
        parsed_url = urlparse(link)
        query_params = parse_qs(parsed_url.query)

        if pattern:
            for key, values in query_params.items():
                if any(pattern in f"{key}={value}" for value in values):
                    filtered.append(link)
                    break
        else:
            if query_params:
                filtered.append(link)

    return filtered

def check_link_status(links):
    valid_links = []
    for link in links:
        try:
            response = requests.head(link, timeout=5)
            if response.status_code == 200:
                valid_links.append(link)
        except requests.RequestException:
            pass

    return valid_links

def save_results(results, filename="parameter.txt"):
    try:
        filename = "parameter.txt"
        
        with open(filename, "w") as f:
            f.writelines([f"[+] {result}\n" for result in results])
        logging.info(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} Results saved to {filename}")
    
    except Exception as e:
        logging.error(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Failed to save results: {e}")

def main():
    print(rf"""
{Fore.YELLOW}
    Coded By GhosT LulzSec
    Telegram : @WW6WW6WW6
    GitHub: https://github.com/69d9
    All rights reserved.

            o  o   o  o
         |\/ \^/ \/|  
         |,-------.|  
       ,-.(|)   (|),-. 
       \_*._ ' '_.* _/  
        /-.--' .-`\  
   ,--./    `---'    \,--. 
   \   |(  )     (  )|   /  
hjw \  |         |  /  
`97  \ | /|\     /|\ | /  
     /  \-._     _,-/  \  
    //| \  `---'  // |\\  
   /,-.,-.\       /,-.,-.\  
  o   o   o      o   o    o  
""")

    try:
        target_url = input(f"{Fore.BLUE}[INPUT]{Style.RESET_ALL} Enter the target URL or domain: ").strip()
        pattern = input(f"{Fore.BLUE}[INPUT]{Style.RESET_ALL} Enter a pattern to filter links (e.g., 'id='), or press Enter to skip: ").strip()

        if not target_url:
            logging.error(f"{Fore.RED}[ERROR]{Style.RESET_ALL} No URL provided. Exiting.")
            return

        logging.info(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} Fetching links from {Fore.CYAN + target_url + Style.RESET_ALL}")
        page_links = fetch_links_from_page(target_url)

        logging.info(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} Found {Fore.GREEN + str(len(page_links)) + Style.RESET_ALL} links.")

        print(f"{Fore.GREEN}[INFO]{Style.RESET_ALL} All extracted links:")
        for link in page_links:
            print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {link}")

        filtered_links = filter_links(page_links, pattern)
        logging.info(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} Found {Fore.GREEN + str(len(filtered_links)) + Style.RESET_ALL} filtered links.")

        valid_links = check_link_status(filtered_links)
        logging.info(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} Found {Fore.GREEN + str(len(valid_links)) + Style.RESET_ALL} valid links.")

        print(f"{Fore.GREEN}[INFO]{Style.RESET_ALL} Valid links:")
        for link in valid_links:
            print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {link}")

        save_results(valid_links, "parameter.txt")

    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[INFO]{Style.RESET_ALL} Execution interrupted by user. Exiting...")
    except Exception as e:
        logging.error(f"{Fore.RED}[ERROR]{Style.RESET_ALL} An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
