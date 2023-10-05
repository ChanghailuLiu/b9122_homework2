import requests
from bs4 import BeautifulSoup

BASE_URL = "https://press.un.org"
SEED_URL = f"{BASE_URL}/en"
MAX_NUM = 10

def get_links_from_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return [a['href'] for a in soup.find_all('a', href=True)]
    except:
        return []

def is_press_release(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    press_release_tag = soup.find('a', {'href': '/en/press-release', 'hreflang': 'en'})
    return press_release_tag is not None

def main():
    visited = set()
    to_visit = [SEED_URL]
    press_releases = []
    while to_visit and len(press_releases) < MAX_NUM:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)
        # Check if the URL is a press release
        if is_press_release(url):
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            if "crisis" in soup.get_text().lower():
                press_releases.append(url)
                print(f"Found press release {len(press_releases)}: {url}")

        # Add new links to the to_visit list
        links = get_links_from_page(url)
        for link in links:
            if link.startswith('/'):
                absolute_url = BASE_URL + link
                if absolute_url not in visited:
                    to_visit.append(absolute_url)

    print("Press releases found:")
    for pr in press_releases:
        print(pr)

if __name__ == "__main__":
   main()

