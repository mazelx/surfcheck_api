import os
import datetime
from pymongo import MongoClient
from abc import ABCMeta, abstractmethod


class AbstractMongoProvider:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        client = MongoClient(os.environ['MONGODB_URI'],
                             connectTimeoutMS=30000,
                             socketTimeoutMS=None,
                             socketKeepAlive=True)

        self._db = client.get_default_database()
        self._current_collection = None

    def map(self, docs):
        return docs

    def latest_one(self, max_dt=0):
        if max_dt == 0:
            return self._current_collection.find({}).sort("datetime", -1).limit(1)[0]
        max_dt = datetime.datetime(max_dt, '%Y%m%d%H%M')
        min_dt = max_dt - datetime.timedelta(minutes=30)
        docs = self._current_collection.find_one({"datetime": {"$lte": max_dt, "$gt": min_dt}}, {"_id": 0})
        return self.map(docs)

    def latest_list(self, max_dt=datetime.datetime.utcnow()):
        min_dt = max_dt - datetime.timedelta(hours=49)
        docs = self._current_collection.find({"datetime": {"$lte": max_dt, "$gt": min_dt}}).sort([("datetime", 1)])
        return self.map(list(docs))


class WavesProvider (AbstractMongoProvider):
    def __init__(self):
        super(WavesProvider, self).__init__()
        self._current_collection = self._db.wave_data


class WeatherProvider(AbstractMongoProvider):
    def __init__(self):
        super(WeatherProvider, self).__init__()
        self._current_collection = self._db.weather_data

    def map(self, docs):
        mapped_docs = []
        for doc in docs:
            try:
                mapped_docs.append({
                        "location": doc["name"],
                        "wind_speed": doc["wind"]["speed"],
                        "wind_deg": doc["wind"]["deg"],
                        "datetime": doc["datetime"]
                  })
            except KeyError:
                print "err on doc : " + str(doc)
        return mapped_docs
