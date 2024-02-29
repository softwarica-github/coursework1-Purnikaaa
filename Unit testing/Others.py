import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

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

def main():
    # Example usage
    user_input = input("Enter the URL (e.g., www.example.com): ")
    webpage_info = WebPageInfo(user_input)

    # 1. Content Type
    content_type = webpage_info.get_content_type()
    if content_type is not None:
        print(f"\n1. Content Type: {content_type}")

    # 2. Metadata Type
    metadata_types = webpage_info.get_metadata_type()
    if metadata_types is not None:
        print(f"2. Metadata Types: {metadata_types}")

    # 3. Cookies
    cookies = webpage_info.get_cookies()
    if cookies is not None:
        print(f"3. Cookies: {cookies}")

    # 4. Headers
    headers = webpage_info.get_headers()
    if headers is not None:
        print("\n4. Headers:")
        for key, value in headers.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()
