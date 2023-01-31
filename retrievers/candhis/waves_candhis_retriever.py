import requests
import os
from datetime import datetime
import logging
from lxml import html
import json 

logger = logging.getLogger()

# candhis parameters
url = "https://candhis.cerema.fr/_public_/campagne.php"

class WaveData:
    def __init__(self, campaign_id, dt, height, height_max, period, direction, spreading, temperature) -> None:
        self.campaign_id = campaign_id
        self.dt = dt
        self.height = height
        self.height_max = height_max
        self.period = period
        self.direction = direction
        self.spreading = spreading
        self.temperature = temperature
        self.validate()

    def validate(self):
        if not (0  <= self.height < 20):
            raise ValueError(f"Error validating wave data attribute : height={self.height}")
        if not (0  <= self.height_max < 20):
            logger.warn(f"Error validating wave data attribute : height_max={self.height_max}")
        if not (0  <= self.period < 50):
            raise ValueError(f"Error validating wave data attribute : period={self.period}")
        if not (0  <= self.direction < 360):
            logger.warn(f"Error validating wave data attribute : direction={self.direction}")
        if not (0  <= self.spreading < 360):
            logger.warn(f"Error validating wave data attribute : spreading={self.spreading}")
        if not (-20  < self.temperature < 40):
            logger.warn(f"Error validating wave data attribute : temperature={self.temperature}")
        
    def to_dict(self) -> dict:
        dict_values = self.__dict__.copy()
        dict_values['dt'] = self.dt.isoformat()
        return dict_values

    def __str__(self) -> str:
        return json.dumps(self.to_dict())

def get_candhis_data(campaign_id):
    logger.debug("Starting candhis data scraping")

    session = requests.session()
    session.get(url)
    r = session.get(f"{url}?{campaign_id}")
    logger.info(url)
    extracts = []

    tree = html.fromstring(r.text) 

    for tr in tree.xpath('//*[@id="idCardCamp"]/div//table[contains(@class, "table")]//tbody/tr'):

        vdict = {}
        values = []

        for td in tr.getchildren():
            try:
                values.append(td.xpath('.//span//text()')[0].strip())
            except:
                pass

        if len(values) != 8:
            if len(values) != 0:
                print("[MALFORMED] " + str(values) + " malformed row")
            continue
        try:
            vdict["campaign_id"] = campaign_id
            vdict["dt"] = datetime.strptime(f"{values[0]} {values[1]}", '%d/%m/%Y %H:%M')
            vdict["height"] = float(values[2])
            vdict["height_max"] = float(values[3])
            vdict["period"] = float(values[4])
            vdict["direction"] = float(values[5])
            vdict["spreading"] = float(values[6])
            vdict["temperature"] = float(values[7])

            extracts.append(WaveData(**vdict))        

        except ValueError:
            logger.debug("[ERROR] Error parsing row : " + str(values))
            continue        
    return extracts

