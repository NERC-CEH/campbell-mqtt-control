"""Utility for parsing setting names from online documentation"""

import requests
from bs4 import BeautifulSoup


def parse_settings(url: str) -> None:
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")

    headers = soup.find_all("h2")

    for h in headers:
        link = h.a
        if link:
            print(link.get("name"))


if __name__ == "__main__":
    url = "https://help.campbellsci.com/CR1000X/Content/shared/Maintain/Advanced/settings-general.htm"
    parse_settings(url)
