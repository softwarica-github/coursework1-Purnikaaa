import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
from bs4 import BeautifulSoup
import ssl
import socket
import datetime
from urllib.parse import urlparse, urljoin
import whois

class WebsiteStatus:
    def __init__(self, url):
        self.url = self.normalize_url(url)

    def normalize_url(self, url):
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

class UrlInfoRetriever:
    def __init__(self):
        pass
    
    def get_ip_address(self, url):
        try:
            ip_address = socket.gethostbyname(url)
            return ip_address
        except socket.gaierror:
            return None

    def get_server_info(self, url):
        try:
            response = requests.head("http://" + url)
            server_info = response.headers.get('server', 'Server information not available')
            return server_info
        except requests.RequestException:
            return None

class WebsiteInfoRetriever:
    def __init__(self):
        pass

    def get_whois_info(self, url):
        try:
            whois_info = whois.whois(url)
            return whois_info
        except whois.parser.PywhoisError:
            return None

class SubdomainRetriever:
    def __init__(self):
        pass

    def get_subdomains_crtsh(self, url):
        try:
            crt_sh_url = f"https://crt.sh/?q={url}&output=json"
            response = requests.get(crt_sh_url)
            if response.status_code == 200:
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
    
class WebPageInfo:
    def __init__(self, url):
        self.url = self.normalize_url(url)

    def normalize_url(self, url):
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
    
def main(user_input):
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
        for key, value in whois_info.items():
            print(f"{key}: {value}")
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
    if metadata_types:
        filtered_metadata_types = filter(None, metadata_types)
        print(f"\n11. Metadata Types: {', '.join(filtered_metadata_types)}")
    else:
        print("\n11. Metadata Types: No metadata types found")

    cookies = web_page_info.get_cookies()
    print(f"\n12. Cookies: {cookies}")

    headers = web_page_info.get_headers()
    print(f"\n13. Headers:")
    for key, value in headers.items():
        print(f"{key}: {value}")



class CustomText(tk.Text):
    def __init__(self, master=None, **kwargs):
        tk.Text.__init__(self, master, **kwargs)
        self.config(state=tk.DISABLED)

    def insert_text_with_heading(self, heading, text):
        self.config(state=tk.NORMAL)
        self.insert(tk.END, f"\n\n{heading}\n")
        self.insert(tk.END, "-" * len(heading) + "\n")
        self.insert(tk.END, text)
        self.config(state=tk.DISABLED)

    def write(self, text):
        self.config(state=tk.NORMAL)
        self.insert(tk.END, text)
        self.config(state=tk.DISABLED)

class WebInfoGUI:
    def __init__(self, master):
        self.master = master
        master.title("Web Information Retrieval Tool")
        master.configure(bg="#f0f0f0")

        # Entry and Button Frame
        entry_frame = tk.Frame(master, bg="#f0f0f0", padx=10, pady=10)
        entry_frame.pack()

        self.label = tk.Label(entry_frame, text="Enter URL:", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12))
        self.label.grid(row=0, column=0, sticky="w", padx=5)

        self.entry = tk.Entry(entry_frame, width=30, bg="white", fg="#333333", bd=2, relief="solid")
        self.entry.grid(row=0, column=1, padx=5)

        self.button = tk.Button(entry_frame, text="Get Information", command=self.retrieve_info, bg="#4CAF50", fg="white", font=("Helvetica", 10), padx=10)
        self.button.grid(row=0, column=2, padx=5)

        self.clear_button = tk.Button(entry_frame, text="Clear", command=self.clear_output, bg="#f44336", fg="white", font=("Helvetica", 10), padx=10)
        self.clear_button.grid(row=0, column=3, padx=5)

        self.quit_button = tk.Button(entry_frame, text="Quit", command=master.destroy, bg="#333333", fg="white", font=("Helvetica", 10), padx=10)
        self.quit_button.grid(row=0, column=4)

        # Text Area
        self.text_area = CustomText(master, wrap=tk.WORD, width=80, height=20, bg="white", fg="#333333", padx=10, pady=10, font=("Courier New", 10), bd=2, relief="solid")
        self.text_area.pack()

    def retrieve_info(self):
        user_input = self.entry.get().strip()
        if not user_input:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return

        self.text_area.delete(1.0, tk.END)

        # Redirect the standard output to the custom text widget
        import sys
        sys.stdout = self.text_area

        # Call the main function with the user input
        main(user_input)

        # Restore the standard output
        sys.stdout = sys.__stdout__

    def clear_output(self):
        self.text_area.config(state=tk.NORMAL)  # Set state to NORMAL before deleting
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)  # Set state back to DISABLED


if __name__ == "__main__":
    root = tk.Tk()
    app = WebInfoGUI(root)
    root.mainloop()

