import bs4


def parse_html(s: str) -> bs4.BeautifulSoup:
    return bs4.BeautifulSoup(s, "html.parser")
