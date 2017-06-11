import requests
import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient()
db = client.surf_check
wave_data = db.wave_data

url = "http://candhis.cetmef.developpement-durable.gouv.fr/campagne/inc-tempsreel.php?idcampagne=" \
      + "f7177163c833dff4b38fc8d2872f1ec6"
r = requests.get(url)
soup = BeautifulSoup.BeautifulSoup(r.text)
extracts = []

for tr in soup.findAll('tr'):
    vdict = {}
    values = [td.text for td in tr.findAll('td')]
    if len(values) != 7:
        print("row malformed : " + str(values))
        continue
    vdict["time"] = datetime.strptime(values[0], '%d/%m/%Y %H:%M')
    vdict["wave_height"] = float(values[1])
    vdict["wave_height_max"] = float(values[2])
    vdict["wave_period"] = float(values[3])
    vdict["wave_direction"] = float(values[4])
    vdict["wave_spreading"] = float(values[5])
    vdict["water_temperature"] = float(values[6])
    try:
        result = wave_data.insert(vdict)
        print("[INSERT] " + str(vdict["time"]) + " ok")
    except DuplicateKeyError:
        print("[DUPLICATE] " + str(vdict["time"]) + " already exist")
