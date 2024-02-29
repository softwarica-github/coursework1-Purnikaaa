import requests
import re
import socket

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

def main():
    subdomain_retriever = SubdomainRetriever()

    # Get URL from the user
    url = input("Enter the URL: ")

    # Get and display subdomains with IP addresses
    subdomains = subdomain_retriever.get_all_subdomains(url)
    if subdomains:
        print("\nSubdomains and their IP Addresses:")
        for subdomain in subdomains:
            ip_address = socket.gethostbyname(subdomain)
            print(f"{subdomain}: {ip_address}")
    else:
        print("Unable to retrieve subdomains.")

if __name__ == "__main__":
    main()
