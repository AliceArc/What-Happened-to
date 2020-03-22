import requests

wiki_url = "https://en.wikipedia.org/wiki/George_Lucas"
response = requests.get(wiki_url)

print(type(str(response.content)))
from bs4 import BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')
from re import sub

page_title = soup.h1.string


headers = soup.find_all('h2')
# header_strings = [elem.string for elem in headers]
# print(header_strings)

ignored_headers = ["Contents", "Early life", "Filmography", "References", "Further reading", "External links", "Navigation menu", "Awards and honors", "Written works"]

for header in headers:
    if header.string in ignored_headers:
        print(f'ignored: {header.string}')
    else:
        print(f'do stuff with: {header.string}')
        next_header = header.find_next_sibling("h2")
        last_elem_in_section = next_header.previous_sibling.previous_sibling
        last_content = last_elem_in_section.get_text()
        last_content = sub(r'\[\d+\]', '', last_content)
        print(last_content)
    print("-"*10)