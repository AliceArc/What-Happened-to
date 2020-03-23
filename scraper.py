# imported libraries
import requests
# beautifulsoup - web scraping tool
from bs4 import BeautifulSoup
# regex - used for dynamic substitutions
from re import sub

# our main variables.
wiki_url = "https://en.wikipedia.org/wiki/{}"
celeb_name = input("Who're you thinkin' about? ")
response = requests.get(wiki_url.format(celeb_name.replace(' ', '_')))

# parse html
soup = BeautifulSoup(response.content, 'html.parser')

# defines where to locate each page title
page_title = soup.h1.string

# finds all sections on wikipedia page
headers = soup.find_all('h2')


# takes a p element & removes wiki references
def process_paragraph(p):
    return sub(r'\[\d+\]', '', p.get_text())


# sections we do not find relevant
ignored_headers = ["contents", "early life", "filmography", "references", "further reading", "external links",
                   "navigation menu", "filmmaking", "bibliography", "contents", "see also", "notes"]


# processes sections we care about by pulling last paragraph/item from every section
for header in headers:
    header_name = (header.string or header.contents[0].string or header.find("span", {"class": "mw-headline"}).string).lower()
    if header_name not in ignored_headers:
        print(f'Current header: {header_name}')
        next_header = header.find_next_sibling("h2")
        # goes back twice because usually first previous sibling is an empty space
        last_tag_in_section = next_header.previous_sibling.previous_sibling
        # depending on what tag you land on, handle it in different ways
        if last_tag_in_section.name == "p":
            last_content = process_paragraph(last_tag_in_section)
            print(last_content)
        # we want tables! prints last item with all relevant information.
        elif last_tag_in_section.name == "table":
            table_body = last_tag_in_section.tbody
            # finds table headers
            table_titles = table_body.tr.find_all("th")
            table_column_count = len(table_titles)
            rows = table_body.find_all("tr")
            row_index = -1
            current_row_td_count = len(rows[row_index].find_all("td"))
            while current_row_td_count < table_column_count:
                row_index -= 1
                current_row_td_count = len(rows[row_index].find_all("td"))
            rows_i_care_about = rows[row_index:-1]
            rows_i_care_about.insert(0, table_body.tr)
            for r in rows_i_care_about:
                print(r.get_text())
        # we dont want quotes -- jumps back again to find p
        elif last_tag_in_section.name == "blockquote":
            content = process_paragraph(last_tag_in_section.find_previous_sibling("p"))
            print(content)
        print

