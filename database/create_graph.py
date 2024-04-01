"""
Store Wikipedia Data in article_name: [list of outgoing articles] format in a dictionary and store in in a JSON file.
"""
import json
from collections import defaultdict
from typing import Any
import requests
from bs4 import BeautifulSoup
import python_ta


def url_to_title(url: str) -> str:
    """Convert the input URL to just the title of the Wikipedia page"""
    last_part = url.split('/')[-1]
    formatted_string = last_part.replace('_', ' ')
    title = formatted_string.title()
    return title

def save_dict_to_file(file_path: str, data: defaultdict[Any, set]) -> None:
    """Save graph data dictionary as a JSON file. If the JSON file already exists, update it instead."""
    try:
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = {}

    # Merge the existing data with the new data
    for key, value in data.items():
        if key in existing_data:
            if isinstance(existing_data[key], set):
                existing_data[key].update(value)
            else:
                existing_data[key] = value
        else:
            existing_data[key] = value

    # Convert sets to lists before writing to file
    for key, value in existing_data.items():
        if isinstance(value, set):
            existing_data[key] = list(value)

    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)


def get_links_in_page(current_url: str) -> list:
    """Return all outgoing links of from the current_url's page using requests and BS4"""
    lst = []
    response = requests.get(current_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('/wiki/') and ':' not in href:
            next_url = 'https://en.wikipedia.org' + href
            lst.append(next_url)
    return lst


def go_through_links_recursive(start: str, visited_f: str, graph_f: str, limit: int, current_level: int = 0) -> None:
    """
    Recursively move through each link and its outgoing links and save their connection in a key value pair.
    The key is the current page, and the values are all of its outgoing links obtained from get_links_in_page.
    Update the graph and visited JSON files accordingly. Save only the number of outgoing links according to limit input
    and stop the program if it finishes traversing through the input level (depth).
    """
    data = defaultdict(set)
    try:
        with open(visited_f, 'r') as f:
            visited = set(json.load(f))
    except FileNotFoundError:
        visited = set()

    current_url = start
    current_title = url_to_title(current_url)
    # uncomment this if we do scrape the entire page's link to reduce run time
    if current_url not in visited:
        visited.add(current_url)

        for link in get_links_in_page(current_url)[:limit]:
            title = url_to_title(link)
            if title != current_title:
                data[current_title].add(title)

    with open(visited_f, 'w') as f:
        json.dump(list(visited), f)
    save_dict_to_file(graph_f, data)

    if current_level < 2:
        for link in get_links_in_page(current_url)[:limit]:
            go_through_links_recursive(link, visited_f, graph_f, limit, current_level + 1)
    elif current_level == 2:
        for link in get_links_in_page(current_url)[:limit]:
            title = url_to_title(link)
            if title != current_title and link not in visited:
                data[title] = set()
                visited.add(link)

        save_dict_to_file(graph_f, data)

# # Example usage
# start_url = 'https://en.wikipedia.org/wiki/University_Of_Toronto'
# go_through_links_recursive(start_url, 'small_visited.json', 'small_graph.json', 15, 2)


if __name__ == '__main__':
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E1136', 'W0221', 'E9998'],
        'extra-imports': ['requests', 'bs4', 'json', 'os', 'collections', 'typing'],
        'max-nested-blocks': 4})
