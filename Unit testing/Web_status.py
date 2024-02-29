import requests
from bs4 import BeautifulSoup
import ssl
import socket
import datetime
from urllib.parse import urlparse, urljoin

class WebsiteStatus:
    def __init__(self, url):
        self.url = self.normalize_url(url)

    def normalize_url(self, url):
        # Add http:// or https:// if not present
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        return url

    def get_website_status(self):
        try:
            response = requests.get(self.url)
            return response.status_code
        except requests.RequestException as e:
            print(f"Error: {e}")
            return None

    def get_http_status(self):
        try:
            response = requests.head(self.url)
            return response.status_code
        except requests.RequestException as e:
            print(f"Error: {e}")
            return None

    def get_last_modification_date(self):
        try:
            response = requests.head(self.url)
            last_modified = response.headers.get('last-modified')
            if last_modified:
                return last_modified
            else:
                return "Last modification date not available."
        except requests.RequestException as e:
            print(f"Error: {e}")
            return None

    def get_ssl_certificate_info(self):
        try:
            hostname = urlparse(self.url).hostname
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    ssl_info = ssock.getpeercert()
                    return ssl_info
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_all_links(self):
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.content, 'html.parser')
            links = [urljoin(self.url, link.get('href')) for link in soup.find_all('a', href=True)]
            return links
        except requests.RequestException as e:
            print(f"Error: {e}")
            return None

def main():
    # Example usage
    user_input = input("Enter the URL (e.g., www.example.com): ")
    website_status_checker = WebsiteStatus(user_input)

    # 1. Website Status
    website_status = website_status_checker.get_website_status()
    if website_status is not None:
        print(f"\n1. Website Status: {website_status}")

    # 2. HTTP Status
    http_status = website_status_checker.get_http_status()
    if http_status is not None:
        print(f"2. HTTP Status: {http_status}")

    # 3. Last Modification Date
    last_modification_date = website_status_checker.get_last_modification_date()
    print(f"3. Last Modification Date: {last_modification_date}")

    # 4. SSL/TLS Certificate
    ssl_certificate_info = website_status_checker.get_ssl_certificate_info()
    if ssl_certificate_info is not None:
        expiration_date = datetime.datetime.strptime(ssl_certificate_info['notAfter'], "%b %d %H:%M:%S %Y %Z")
        print(f"4. SSL/TLS Certificate Expiration Date: {expiration_date}")

    # 5. All Links
    all_links = website_status_checker.get_all_links()
    if all_links is not None:
        print("\n5. All Links:")
        for link in all_links:
            print(link)

if __name__ == "__main__":
    main()
