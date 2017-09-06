import unittest
from api.data_provider import WavesProvider


class TestWaveProvider(unittest.TestCase):
    def test_latest_one(self):
        waves = WavesProvider()
        result = waves.latest_one()
        self.assertIsNotNone(result)
