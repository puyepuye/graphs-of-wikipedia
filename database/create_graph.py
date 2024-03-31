import requests
from bs4 import BeautifulSoup
import json
import os
from collections import defaultdict

def url_to_title(url: str) -> str:
    # Step 1: Extract the last part of the URL
    last_part = url.split('/')[-1]

    # Step 2: Replace underscores with spaces
    formatted_string = last_part.replace('_', ' ')

    # Step 3: Capitalize the first letter of each word
    title = formatted_string.title()

    return title

def save_dict_to_file(file_path, data):
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


def load_dict_from_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)
    else:
        return {}

def get_links_in_page(current_url):
    # Make a request to the current URL
    lst = []
    response = requests.get(current_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('/wiki/') and ':' not in href:
            next_url = 'https://en.wikipedia.org' + href
            lst.append(next_url)
    return lst

def go_through_links_recursive(start_url, visited_file, graph_file, limit, level, current_level=0):
    visited = set()
    data = defaultdict(set)
    try:
        with open(visited_file, 'r') as f:
            visited = set(json.load(f))
    except FileNotFoundError:
        pass

    current_url = start_url
    current_title = url_to_title(current_url)
    # uncomment this if we do scrape the entire page's link to reduce run time
    if current_url not in visited:
        visited.add(current_url)

        for link in get_links_in_page(current_url)[:limit]:
            title = url_to_title(link)
            if title != current_title:
                data[current_title].add(title)

        print(current_url)
    with open(visited_file, 'w') as f:
        json.dump(list(visited), f)
    save_dict_to_file(graph_file, data)

    if current_level < level:
        for link in get_links_in_page(current_url)[:limit]:
            print(current_level)
            go_through_links_recursive(link, visited_file, graph_file, limit, level, current_level + 1)
    elif current_level == level:
        for link in get_links_in_page(current_url)[:limit]:
            title = url_to_title(link)
            if title != current_title and link not in visited:
                data[title] = set()
                visited.add(link)

        save_dict_to_file(graph_file, data)

# Example usage
start_url = 'https://en.wikipedia.org/wiki/University_Of_Toronto'
go_through_links_recursive(start_url, 'small_visited.json', 'small_graph.json', 15, 2)
