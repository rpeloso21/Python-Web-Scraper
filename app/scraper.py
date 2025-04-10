import requests
from bs4 import BeautifulSoup
import os
import socket
from urllib.parse import urlparse

def is_domain_resolvable(url):
    try:
        domain = urlparse(url).netloc
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        print(f"DNS resolution failed for {url}")
        return False

def scrape_links(filepath, keywords):
    relevant_links = []

    with open(filepath, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

        for url in urls:
            url = url.strip()
            if not url:
                continue
            if not url.startswith("http"):
                url = "https://" + url  # Add default scheme
            if not is_domain_resolvable(url):
                continue  # Skip this URL if DNS fails

            try:
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text().lower()

                if any(keyword.lower() in text for keyword in keywords):
                    relevant_links.append(url)

            except Exception as e:
                print(f"Error scraping {url}: {e}")

        
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    result_folder = os.path.join(BASE_DIR, 'results')
    os.makedirs(result_folder, exist_ok=True)
    result_path = os.path.join(result_folder, 'output.txt')

    with open(result_path, 'w') as f:
        for link in relevant_links:
            f.write(link + '\n')


    return result_path