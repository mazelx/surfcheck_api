import requests
import os
import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import logging
from logging.handlers import RotatingFileHandler


def main():
    # logging to file
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    ## logging to file
    #formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    #file_handler = RotatingFileHandler('/var/log/surfcheck/candhis_data.log', 'a', 1000000, 1)
    #file_handler.setLevel(logging.INFO)
    #file_handler.setFormatter(formatter)
    #logger.addHandler(file_handler)

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
    wave_data = db.wave_data

    # candhis parameters
    url = "http://candhis.cetmef.developpement-durable.gouv.fr/campagne/inc-tempsreel.php?idcampagne=" \
          + "6c8349cc7260ae62e3b1396831a8398f"
    r = requests.get(url)
    soup = BeautifulSoup.BeautifulSoup(r.text)
    extracts = []

    logger.debug("Starting candhis data scraping")
    for tr in soup.findAll('tr'):
        vdict = {}
        values = [td.text for td in tr.findAll('td')]
        if len(values) != 7:
            if len(values) != 0:
                print("[MALFORMED] " + str(values) + " malformed row")
            continue
        vdict["datetime"] = datetime.strptime(values[0], '%d/%m/%Y %H:%M')
        vdict["wave_height"] = float(values[1])
        vdict["wave_height_max"] = float(values[2])
        vdict["wave_period"] = float(values[3])
        vdict["wave_direction"] = float(values[4])
        vdict["wave_spreading"] = float(values[5])
        vdict["water_temperature"] = float(values[6])
        try:
            result = wave_data.insert(vdict)
            extracts.append(result)
            logger.debug("[INSERT] " + str(vdict["datetime"]) + " ok")
        except DuplicateKeyError:
            logger.debug("[DUPLICATE] " + str(vdict["datetime"]) + " already exist")
            pass

    logger.info("Finished, " + str(len(extracts)) + " documents inserted")

