import requests
import bs4
from typing import Tuple
from bs4 import BeautifulSoup
import json

class Wiki_container:

    def __init__(self) -> None:
        self._data = {}
        self.code_name_map = {}
        self.format_code_map = {}


def get_data_maps() -> Wiki_container:
    container = Wiki_container()
    res = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes')
    soup = BeautifulSoup(res.content, 'html.parser')
    table = soup.find('table', class_='wikitable sortable')
    for row in table.tbody.find_all('tr'):
        process_row(container, row)
    return container


def process_row(container: Wiki_container, row: bs4.element.Tag) -> Wiki_container:
    column = row.find_all('td')
    if column and column[3].text.strip() != '- no codes -':
        row_tuple = (column[0].a.get('href'), column[0].text.strip(), column[2].text.strip(), column[3].text.strip(), column[4].text.strip(), column[5].text.strip())
        add_all_data(row_tuple, container)
        container.code_name_map.update({row_tuple[2]: row_tuple[1]})
        container.format_code_map.setdefault(row_tuple[3], [])
        container.format_code_map[row_tuple[3]].append(row_tuple[2])

    return container


def add_all_data(row_tuple: Tuple, container: Wiki_container):
    iso = row_tuple[2]
    container._data.setdefault(iso, {})
    container._data[iso].update({'country': row_tuple[1]})
    container._data[iso].update({'country_link': row_tuple[0]})
    container._data[iso].update({'area_format': row_tuple[3]})
    container._data[iso].update({'street_format': row_tuple[4]})


def dump_container(container: Wiki_container):
    with open('./data/data.json', 'w') as f:
        json.dump(container._data, f, indent='\t', )

    with open('./data/country_code_name_map.json', 'w') as f:
        json.dump(container.code_name_map, f, indent='\t')

    with open('./data/format_country_code_map.json', 'w') as f:
        json.dump(container.format_code_map, f, indent='\t')


def main():
    container = get_data_maps()
    dump_container(container)


if __name__ == "__main__":
    main()
