import requests
import json
import re

API_URL = 'https://entropia.de/api.php?format=json&action=parse&page=Vorlage:Termine'

class WikiTermine:
    def __init__(self, data):
        self.__html = data['parse']['text']['*'].replace("\n", "")
        self.parse_rows()
        self.parse_events()

    def parse_rows(self):
        row_re = re.compile("<tr>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?</tr>")
        self.__rows = row_re.finditer(self.__html, re.I)

    def strip_html(self, data):
        return re.sub('<[^<]+?>', '', data)

    def parse_events(self):
        self.__events = []
        for row in self.__rows:
            date, time, place, desc = [self.strip_html(col).strip() for col in row.groups()]
            self.__events.append(dict(date=date, time = time, place=place, desc=desc))

    def to_json_file(self, filename):
        with file(filename, 'wb') as f:
            f.write(json.dumps(self.events, ensure_ascii=False).encode('utf8'))

    @property
    def events(self):
        return self.__events

if __name__ == '__main__':
    r = requests.get(API_URL)
    termine = WikiTermine(r.json())
    termine.to_json_file('termine.json')
