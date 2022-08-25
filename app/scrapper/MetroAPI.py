from typing import Union

import requests


class MetroAPI:
    def __init__(self, token, api_url):
        if not token or not api_url:
            raise "Missing arguments"

        self.api_url = api_url
        self.token = token

    def call_api(self, endpoint) -> Union[dict, str]:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/104.0.5112.81 Safari/537.36 "
        headers = {
            'content-type': 'application/json',
            'user-agent': user_agent,
            'Authorization': 'Bearer ' + self.token
        }

        # request for HTML document of given url
        response = requests.get(self.api_url + endpoint, headers=headers)

        # response will be provided in JSON format
        return response.json()

    def get_station_info(self):
        result = self.call_api("infoEstacao/todos")

        # Convert to db models
        stations: list = result["resposta"]

        def lineConv(line_raw):
            return {
                "Verde": 'GREEN',
                "Vermelha": 'RED',
                "Amarela": 'YELLOW',
                "Azul": 'BLUE'
            }[line_raw]

        def parse_api_station(stop):
            import re

            raw_lines = stop['linha']
            raw_lines = re.sub(r"[\[\]]", "", raw_lines)
            raw_lines = raw_lines.split(",")
            raw_lines = [x.strip() for x in raw_lines]
            raw_lines = [lineConv(x) for x in raw_lines]

            station_obj = {
                "code": stop["stop_id"],
                "lat": stop["stop_lat"],
                "lon": stop["stop_lon"],
                "name": stop["stop_name"],
                "lines": raw_lines
            }
            return station_obj

        stations = [parse_api_station(stop) for stop in stations]
        return stations

    def get_destination_info(self):
        api = self.call_api("infoDestinos/todos")
        return api['resposta']

    def get_line_sate(self):
        return self.call_api("estadoLinha/todos")

    def get_waiting_time(self):
        result = self.call_api("/tempoEspera/Estacao/todos")
        return result

    def get_station_time(self, station_code, destination=None):
        result = self.call_api("/tempoEspera/Estacao/" + station_code)['resposta']

        if destination:
            return [next(filter(lambda x: "destino" in x and x["destino"] == destination, result), None)]

        return result
