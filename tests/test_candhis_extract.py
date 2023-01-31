import unittest
from retrievers.candhis.waves_candhis_retriever import get_candhis_data

campaign_id = 'Y2FtcD0wNjQwMg=='

class TestCandhisRetriever(unittest.TestCase):
    def test_site_up(self):
        get_candhis_data(campaign_id)
    
    def test_has_data(self):
        results = get_candhis_data(campaign_id)
        self.assertTrue(len(results)>0)

    def test_to_dict(self):
        results = get_candhis_data(campaign_id)
        results[0].to_dict()
