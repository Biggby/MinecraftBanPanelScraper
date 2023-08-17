import requests
import time
import sys
from bs4 import BeautifulSoup

class TeeStream:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)

def find_links_with_keyword(url, keyword):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        matching_links = []

        for link in links:
            if keyword.lower() in link.text.lower() or keyword.lower() in link['href'].lower():
                matching_links.append(link['href'])

        return matching_links
    else:
        print(f"Failed to fetch the URL: {url}")
        return []

if __name__ == "__main__":
    base_url = "" # Fill in with ban panel link
    keyword_to_find = ""  # Replace with your desired keyword

    # Create and open the "Bans.txt" file in write mode
    with open("Bans.txt", "w") as file:
        # Redirect stdout to both the console and the file using custom TeeStream
        tee_stream = TeeStream(sys.stdout, file)
        sys.stdout = tee_stream

        for page_number in range(1, 3507):  # Change the amount of ban panel pages exist
            page_url = f"{base_url}?page={page_number}"
            matching_links = find_links_with_keyword(page_url, keyword_to_find)

            print(f"Links from {page_url}:")
            for link in matching_links:
                print(link)

            # Adds delay between pay searching
            time.sleep(2)
