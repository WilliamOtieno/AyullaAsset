import unittest
from unittest.mock import patch, Mock
from ..services import get_top_ranked_currencies, search_coin, get_coin_info


class TestCryptoServices(unittest.TestCase):

    @patch('apps.core.services.requests.get')
    def test_get_top_ranked_currencies(self, mock_get):
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = [
            {"name": "Bitcoin", "symbol": "BTC"},
            {"name": "Ethereum", "symbol": "ETH"}
            # Add more example data here
        ]
        mock_get.return_value = mock_response

        result = get_top_ranked_currencies()

        self.assertTrue(mock_response.ok)
        self.assertEqual(len(result), 2)  # Check if the expected number of coins is returned
        self.assertEqual(result[0]['name'], "Bitcoin")

    @patch('apps.core.services.requests.get')
    def test_search_coin(self, mock_get):
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "coins": [
                {"name": "Bitcoin", "symbol": "BTC"},
                {"name": "Bitcoin Cash", "symbol": "BCH"}
            ]
        }
        mock_get.return_value = mock_response

        result = search_coin("Bitcoin")

        self.assertTrue(mock_response.ok)
        self.assertEqual(len(result), 2)  # Check if the expected number of search results is returned
        self.assertEqual(result[0]['symbol'], "BTC")

    @patch('apps.core.services.requests.get')
    def test_get_coin_info(self, mock_get):
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "name": "Bitcoin",
            "symbol": "BTC",
            "description": "A peer-to-peer electronic cash system." 
        }
        mock_get.return_value = mock_response

        result = get_coin_info("bitcoin")

        self.assertTrue(mock_response.ok)
        self.assertEqual(result['name'], "Bitcoin")
        self.assertIn('description', result)


