import requests

# 'https://www.metrolisboa.pt/viajar/proximoscomboios/',
# for station in response.css('#estacao_tempo_espera option'):
# 'station_code': station.xpath('@value'),
from bs4 import BeautifulSoup


# class Line(Enum):
#     YELLOW = 1
#     RED = 2
#     BLUE = 3
#     GREEN = 4
#
#
# @dataclass
# class Station:
#     name: str
#     code: str
#     lat: float
#     lon: float
#     lines: List[Line]
#     timings: Optional[list] = None
#
#     def __repr__(self):
#         return f'{self.name} ({self.code}) - {self.timings[0] if self.timings else "No trams available"}'
from app.db.models.station import Station


def get_html_document(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/104.0.5112.81 Safari/537.36 "
    headers = {
        'content-type': 'application/json',
        'user-agent': user_agent,
    }
    # request for HTML document of given url
    response = requests.get(url, headers=headers)

    # response will be provided in JSON format
    return response.text


# assign required credentials
# assign URL
url_to_scrape = "https://www.metrolisboa.pt/viajar/proximoscomboios/"

# create document
html_document = get_html_document(url_to_scrape)

# create soap object
soup = BeautifulSoup(html_document, 'html.parser')

# find all the anchor tags with "href"
# attribute starting with "https://"


#  = soup.find_all("script", string=re.compile("xhr\\.setRequestHeader\\(\"Authorization\","))
# print(find)
stations = [Station(option.get_text(), option.get('value')) for option in soup.select("#estacao_tempo_espera option")]
stations = [x for x in stations if x.code != '']

for station in stations:
    new_link = url_to_scrape + "?estacao=" + stations[0].code
    html = get_html_document(url_to_scrape)
    new_soup = BeautifulSoup(html, 'html.parser')
    next_timings = new_soup.select("#resultado ul")
    station.timings = next_timings
    print(station)


