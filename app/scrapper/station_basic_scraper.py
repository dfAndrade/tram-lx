import json
import re

import requests
# 'https://www.metrolisboa.pt/viajar/proximoscomboios/',
# for station in response.css('#estacao_tempo_espera option'):
# 'station_code': station.xpath('@value'),
from bs4 import BeautifulSoup

from MetroAPI import MetroAPI
from app.db.SQLiteAdapter import get_db
from app.schemas.stations import Station, get_station_by_name, get_station_by_id


def jprint(json_obj):
    print(json.dumps(json_obj, indent=4, sort_keys=True, default=lambda x: x.value))


def find_token_final():
    token_gen = "https://www.metrolisboa.pt/viajar/proximoscomboios/?estacao=" + "RT"
    return find_token(token_gen)


def find_token(token_gen):
    html = get_html_document(token_gen)
    new_soup = BeautifulSoup(html, 'html.parser')
    pattern = re.compile(r"xhr.setRequestHeader\(\"Authorization\", \"Bearer (.+)\"\);")
    script = new_soup.find('script', text=pattern)
    if script:
        match = pattern.search(script.text)
        if match:
            token = match.group(1)
            return token


def api_call(url, token):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/104.0.5112.81 Safari/537.36 "
    headers = {
        'content-type': 'application/json',
        'user-agent': user_agent,
        'Authorization': 'Bearer ' + token
    }
    # request for HTML document of given url
    response = requests.get(url, headers=headers)

    # response will be provided in JSON format
    try:
        return response.json()
    except:
        return response.text


def station_info_all(token):
    url = "https://api.metrolisboa.pt:8243/estadoServicoML/1.0.0/infoEstacao/todos"
    return api_call(url, token)


def destination_info(token):
    url = "https://api.metrolisboa.pt:8243/estadoServicoML/1.0.1/infoDestinos/todos"
    return api_call(url, token)


def line_state(line_code, token):
    """
    Provides same info as `all` alternative
    :param line_code:
    :param token:
    :return:
    """
    url = "https://api.metrolisboa.pt:8243/estadoServicoML/1.0.0/estadoLinha/" + line_code
    return api_call(url, token)


def line_sate_all(token):
    url = "https://api.metrolisboa.pt:8243/estadoServicoML/1.0.0/estadoLinha/todos"
    return api_call(url, token)


def get_station_timings_all(token):
    url = "https://api.metrolisboa.pt:8243/estadoServicoML/1.0.0/tempoEspera/Estacao/todos"
    return api_call(url, token)


def get_station_timings(station_code):
    token_gen = "https://www.metrolisboa.pt/viajar/proximoscomboios/?estacao=" + station_code
    token = find_token(token_gen)
    url = "https://api.metrolisboa.pt:8243/estadoServicoML/1.0.0/tempoEspera/Estacao/" + station_code
    return api_call(url, token)


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
stations = [Station(name=option.get_text(), code=option.get('value'), lines=[]) for option in
            soup.select("#estacao_tempo_espera option")]
stations = [x for x in stations if x.code != '']

# my_token = find_token()

# print(my_token)


# "https://api.metrolisboa.pt:8243/estadoServicoML/1.0.0/tempoEspera/Estacao/"
# api_call(url_to_scrape + "?estacao=" + stations[0].code)
# for station in stations:
#     new_link = url_to_scrape + "?estacao=" + stations[0].code
#     html = get_html_document(url_to_scrape)
#     new_soup = BeautifulSoup(html, 'html.parser')
#     directions = new_soup.select("#resultado ul li")
#     print(directions)
#     station.timings = next_timings
#     print(station.dict())

# Find timings
# new_link = url_to_scrape + "?estacao=" + stations[0].code
# html = get_html_document(url_to_scrape)
# new_soup = BeautifulSoup(html, 'html.parser')
# directions = new_soup.select("#resultado ul li")

# timings = get_station_timings(stations[0].code)

# timings = get_station_timings_all(stations[0].code)

session_token = find_token_final()
# result = line_sate_all(session_token)
# result = line_state("verde", session_token)
# result = destination_info(session_token)
api_url = "https://api.metrolisboa.pt:8243/estadoServicoML/1.0.1/"
metro_api = MetroAPI(token=session_token, api_url=api_url)

# Get station info
station_info = metro_api.get_station_info()

# station_info_json = [x.json() for x in station_info]

# jprint(station_info)

station_ids = metro_api.get_destination_info()

# jprint(station_ids)

# Populate ids
for id_obj in station_ids:
    station = get_station_by_name(station_info, id_obj['nome_destino'])
    if station:
        station['id'] = id_obj['id_destino']

# jprint(station_info)

db = next(get_db())

# for station in station_info:
#     crud.create_station(db, StationCreate.parse_obj(station))
timings = metro_api.get_station_time("AM", "60")
timings_sa = metro_api.get_station_time("SA", "60")

if timings is not None:
    for stop in timings:
        station = get_station_by_id(station_info, stop['destino'])
        stop['destino'] = station["name"]
# timings = metro_api.get_station_time("SA")

jprint(timings)
jprint(timings_sa)
