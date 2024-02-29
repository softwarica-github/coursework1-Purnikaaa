import whois

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

def main():
    website_info_retriever = WebsiteInfoRetriever()

    # Get URL from the user
    url = input("Enter the URL: ")

    # Get and display WHOIS information
    whois_info = website_info_retriever.get_whois_info(url)
    if whois_info:
        print("WHOIS Information:")
        print(whois_info)
    else:
        print("Unable to get WHOIS information.")

if __name__ == "__main__":
    main()




