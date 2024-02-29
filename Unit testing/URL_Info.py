import socket
import requests

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

def main():
    url_info_retriever = UrlInfoRetriever()
    # Get URL from the user
    url = input("Enter the URL: ")
    # Get and display IP address
    ip_address = url_info_retriever.get_ip_address(url)
    if ip_address:
        print(f"IP Address: {ip_address}")
    else:
        print("Unable to get IP address.")
    # Get and display server information
    server_info = url_info_retriever.get_server_info(url)
    if server_info:
        print(f"Server Information: {server_info}")
    else:
        print("Unable to get server information.")

if __name__ == "__main__":
    main()
