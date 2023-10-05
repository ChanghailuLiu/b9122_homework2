import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.europarl.europa.eu"
SEED_URL = f"{BASE_URL}/news/en/press-room"
MAX_NUM = 10

def get_links_from_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return [a['href'] for a in soup.find_all('a', href=True)]
    except:
        return []

def is_plenary_session(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    press_release_tag = soup.find('span', string="Plenary session")
    return press_release_tag is not None

def main():
    visited = set()
    to_visit = [SEED_URL]
    plenary_session = []

    while to_visit and len(plenary_session) < MAX_NUM:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)
        # Check if the URL is a press release
        if is_plenary_session(url):
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            if "crisis" in soup.get_text().lower():
                plenary_session.append(url)
                print(f"Found plenary session {len(plenary_session)}: {url}")

        # Add new links to the to_visit list
        links = get_links_from_page(url)
        for link in links:
            if link.startswith('/'):
                absolute_url = BASE_URL + link
                if absolute_url.startswith(SEED_URL+'/'):
                    if absolute_url not in visited:
                        to_visit.append(absolute_url)
            else:
                absolute_url = link
                if absolute_url.startswith(SEED_URL+'/'):
                    if absolute_url not in visited:
                        to_visit.append(absolute_url)
    print("Plenary session found:")
    for pr in plenary_session:
        print(pr)

if __name__ == "__main__":
   main()



