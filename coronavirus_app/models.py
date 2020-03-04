import datetime
import json
import os
import re

from bs4 import BeautifulSoup
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import (
    Column, Date, Float, ForeignKey, Integer, String, create_engine,
)


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id =  Column(Integer, primary_key=True)

db_file = 'coronavirus_app/resources/sqlite.db'
engine = create_engine(f'sqlite:///{db_file}', echo=True)
Base = declarative_base(cls=Base)


class Patient(Base):
    name = Column(String)
    history_text = Column(String)
    source = Column(String)


class Place(Base):
    name = Column(String)
    lat = Column(Float)
    lng = Column(Float)


class History(Base):
    patient_id = Column(Integer, ForeignKey('patient.id'))
    place_id = Column(Integer, ForeignKey('place.id'))
    date = Column(Date)


RES = []

def parse_info_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')
    hist_divs = soup.find_all('div', class_='item')
    histories = []
    date = None
    while hist_divs:
        text = hist_divs[0].text
        matches = re.match('^・(\d+)/(\d+)', text)
        if matches:
            date = datetime.date(2020, int(matches.group(1)), int(matches.group(2)))
        elif date:
            histories.append((date, text))
        hist_divs = hist_divs[1:]
    link = links[0]['href'] if links else ''
    return link, histories


def load_data():
    with open('coronavirus_app/resources/rawData.json') as f:
        data = json.loads(f.read())
    all_hist = []
    for item in data:
        title = item['title']
        link, histories = parse_info_html(item['infoWindowContent'])
        for date, event in histories:
            lat = item['pos']['lat']
            lng = item['pos']['lng']
            assert lat and lng
            all_hist.append({
                'title': title,
                'lat': lat,
                'lng': lng,
                'date': date.isoformat(),
                'event': event,
                'link': link,
            })
    return all_hist


def reset_db():
    if os.path.exists(db_file):
        os.remove(db_file)
    Base.metadata.create_all(engine)


def feed_data():
    histories = load_data()
    with open('coronavirus_app/resources/events.json', 'w') as f:
        f.write(json.dumps(histories, indent=2))


if __name__ == '__main__':
    feed_data()
