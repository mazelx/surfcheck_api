import unittest
from api.data_provider import WavesProvider, WeatherProvider


class TestWaveProvider(unittest.TestCase):
    def test_wave_latest_one(self):
        waves = WavesProvider()
        result = waves.latest_one()
        print(result)
        self.assertIsNotNone(result)


class TestWeatherProvider(unittest.TestCase):
    def test_weather_latest_one(self):
        weather = WeatherProvider()
        result = weather.latest_one()
        print(result)
        self.assertIsNotNone(result)
