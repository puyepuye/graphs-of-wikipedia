import requests
from bs4 import BeautifulSoup

def get_links_in_page(current_url):
    # Make a request to the current URL
    lst = []
    response = requests.get(current_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('/wiki/'):
            next_url = 'https://en.wikipedia.org' + href
            lst.append(next_url)
    return lst

if __name__ == '__main__':
    len(get_links_in_page('https://en.wikipedia.org/wiki/University_Of_Toronto'))