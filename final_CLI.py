import tkinter as tk
from tkinter import scrolledtext
import requests
from bs4 import BeautifulSoup
import ssl
import socket
import datetime
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
import re
import whois

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


########################################### URL ######################################################



class UrlInfoRetriever:
    def __init__(self):
        pass
    def get_ip_address(self, url):
        try:
            # Get IP address from the URL
            ip_address = socket.gethostbyname(url)
            return ip_address
        except socket.gaierror:
            return None
    def get_server_info(self, url):
        try:
            # Send a HEAD request to get server information
            response = requests.head("http://" + url)
            server_info = response.headers.get('server', 'Server information not available')
            return server_info
        except requests.RequestException:
            return None

########################################## WHOIS ############################################################

class WebsiteInfoRetriever:
    def __init__(self):
        pass

    def get_whois_info(self, url):
        try:
            # Get WHOIS information for the URL
            whois_info = whois.whois(url)
            return whois_info
        except whois.parser.PywhoisError:
            return None

########################################## SUB DOMAINS ######################################################

class SubdomainRetriever:
    def __init__(self):
        pass

    def get_subdomains_crtsh(self, url):
        try:
            # Fetch subdomains using crt.sh
            crt_sh_url = f"https://crt.sh/?q={url}&output=json"
            response = requests.get(crt_sh_url)
            if response.status_code == 200:
                # Parse JSON response
                json_data = response.json()
                subdomains = set()
                for entry in json_data:
                    subdomains.add(entry['name_value'].strip())
                return list(subdomains)
        except requests.RequestException as e:
            print(f"Error: {e}")
        return None

    def get_subdomains_socket(self, url):
        try:
            # Fetch subdomains using socket
            cname_record = socket.gethostbyname(url)
            subdomains = [cname_record] if cname_record != url else []
            return subdomains
        except socket.gaierror:
            print(f"Domain not found: {url}")
        except Exception as e:
            print(f"Error: {e}")
        return None

    def get_all_subdomains(self, url):
        subdomains_crtsh = self.get_subdomains_crtsh(url) or []
        subdomains_socket = self.get_subdomains_socket(url) or []
        return list(set(subdomains_crtsh + subdomains_socket))

########################################## OTHERS ###########################################################

class WebPageInfo:
    def __init__(self, url):
        self.url = self.normalize_url(url)

    def normalize_url(self, url):
        # Add http:// or https:// if not present
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        return url

    def get_content_type(self):
        try:
            response = requests.head(self.url)
            content_type = response.headers.get('Content-Type')
            return content_type
        except requests.RequestException as e:
            print(f"Error: {e}")
            return None

    def get_metadata_type(self):
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.content, 'html.parser')
            meta_tags = soup.find_all('meta')
            metadata_types = [meta.get('name') or meta.get('property') for meta in meta_tags]
            return metadata_types
        except requests.RequestException as e:
            print(f"Error: {e}")
            return None

    def get_cookies(self):
        try:
            response = requests.get(self.url)
            cookies = response.cookies
            return cookies
        except requests.RequestException as e:
            print(f"Error: {e}")
            return None

    def get_headers(self):
        try:
            response = requests.head(self.url)
            headers = response.headers
            return headers
        except requests.RequestException as e:
            print(f"Error: {e}")
            return None


     
################################################### MAIN PART ##########################################

def main():
    # Example usage
    user_input = input("Enter the URL : ")

    # Website Status
    website_status_checker = WebsiteStatus(user_input)
    website_status = website_status_checker.get_website_status()
    if website_status is not None:
        print(f"\n1. Website Status: {website_status}")

    # HTTP Status
    http_status = website_status_checker.get_http_status()
    if http_status is not None:
        print(f"2. HTTP Status: {http_status}")

    # Last Modification Date
    last_modification_date = website_status_checker.get_last_modification_date()
    print(f"3. Last Modification Date: {last_modification_date}")

    # SSL/TLS Certificate
    ssl_certificate_info = website_status_checker.get_ssl_certificate_info()
    if ssl_certificate_info is not None:
        expiration_date = datetime.datetime.strptime(ssl_certificate_info['notAfter'], "%b %d %H:%M:%S %Y %Z")
        print(f"4. SSL/TLS Certificate Expiration Date: {expiration_date}")

    # All Links
    all_links = website_status_checker.get_all_links()
    if all_links is not None:
        print("\n5. All Links:")
        for link in all_links:
            print(link)

    # URL Info
    url_info_retriever = UrlInfoRetriever()
    ip_address = url_info_retriever.get_ip_address(user_input)
    if ip_address:
        print(f"\n6. IP Address: {ip_address}")
    else:
        print("Unable to get IP address.")

    server_info = url_info_retriever.get_server_info(user_input)
    if server_info:
        print(f"7. Server Information: {server_info}")
    else:
        print("Unable to get server information.")

    # WHOIS Info
    website_info_retriever = WebsiteInfoRetriever()
    whois_info = website_info_retriever.get_whois_info(user_input)
    if whois_info:
        print("\n8. WHOIS Information:")
        print(whois_info)
    else:
        print("Unable to get WHOIS information.")

    # Subdomains Info
    subdomain_retriever = SubdomainRetriever()
    subdomains = subdomain_retriever.get_all_subdomains(user_input)
    if subdomains:
        print("\n9. Subdomains and their IP Addresses:")
        for subdomain in subdomains:
            ip_address = url_info_retriever.get_ip_address(subdomain)
            print(f"{subdomain}: {ip_address}")
    else:
        print("Unable to retrieve subdomains.")

    # Other Info
    web_page_info = WebPageInfo(user_input)
    content_type = web_page_info.get_content_type()
    print(f"\n10. Content Type: {content_type}")

    metadata_types = web_page_info.get_metadata_type()
    print(f"11. Metadata Types: {metadata_types}")

    cookies = web_page_info.get_cookies()
    print(f"12. Cookies: {cookies}")

    headers = web_page_info.get_headers()
    print(f"13. Headers: {headers}")


if __name__ == "__main__":
    main()

