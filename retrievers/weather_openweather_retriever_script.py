import requests
import os
from requests import exceptions
from datetime import datetime
from pymongo import MongoClient
import logging
from logging.handlers import RotatingFileHandler


def main():
    # logging to file
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # logging to file
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    file_handler = RotatingFileHandler('/var/log/surfcheck/openweather_data.log', 'a', 1000000, 1)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # loggging to console
    steam_handler = logging.StreamHandler()
    steam_handler.setLevel(logging.DEBUG)
    logger.addHandler(steam_handler)

    # db access
    client = MongoClient(os.environ['MONGODB_URI'],
                         connectTimeoutMS=30000,
                         socketTimeoutMS=None,
                         socketKeepAlive=True)
    db = client.get_default_database()
    weather_data = db.weather_data

    # openweather parameters
    api_url = "http://api.openweathermap.org/data/2.5/weather?"
    location = "Biarritz,fr"
    appid = "e30f8cfd339545060d2d87d93a8f1afc"
    url = api_url + "q=" + location + "&appid=" + appid

    logger.debug("Connecting to openweathermap.org")
    r = requests.get(url)
    if r.status_code != 200:
        logger.error("error retrieving data with request " + url + " (status code : " + r.status_code + ")")
        raise exceptions.ConnectionError(r.text)

    logger.debug("Query succeeded (" + str(r.status_code) + ")")
    data = r.json()
    data["datetime"] = datetime.today()
    result = weather_data.insert(data)
    logger.info("Data inserted for " + location + " for datetime: " + str(data["datetime"]))


if __name__ == '__main__':
    main()