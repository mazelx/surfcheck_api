import requests
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient()
db = client.surf_check
weather_data = db.weather_data

url = "http://api.openweathermap.org/data/2.5/weather?" \
 	  + "q=Biarritz,fr" \
 	  + "&appid=e30f8cfd339545060d2d87d93a8f1afc"
r = requests.get(url)
data = r.json()
data["datetime"] = datetime.today()
result = weather_data.insert(data)