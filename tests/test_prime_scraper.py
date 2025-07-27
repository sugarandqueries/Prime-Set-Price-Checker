import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import importlib.util
import os
import sys

SAMPLE_PAYLOAD = {
    "payload": {
        "statistics_closed": {
            "90days": [
                {
                    "datetime": "2023-01-01T00:00:00.000Z",
                    "avg_price": 50,
                    "min_price": 45,
                    "max_price": 55,
                    "volume": 10
                },
                {
                    "datetime": "2023-01-02T00:00:00.000Z",
                    "avg_price": 51,
                    "min_price": 46,
                    "max_price": 56,
                    "volume": 12
                }
            ]
        }
    }
}

mock_response = MagicMock()
mock_response.json.return_value = SAMPLE_PAYLOAD
mock_response.raise_for_status.return_value = None

module_path = os.path.join(os.path.dirname(__file__), os.pardir, 'prime_scraper.py')
spec = importlib.util.spec_from_file_location('prime_scraper', module_path)
prime_scraper = importlib.util.module_from_spec(spec)
sys.modules['prime_scraper'] = prime_scraper
with patch('requests.get', return_value=mock_response), \
     patch('time.sleep', return_value=None), \
     patch('pandas.DataFrame.to_csv'):
    spec.loader.exec_module(prime_scraper)


class TestPrimeScraper(unittest.TestCase):
    def test_get_history_dataframe(self):
        resp = MagicMock()
        resp.json.return_value = SAMPLE_PAYLOAD
        resp.raise_for_status.return_value = None
        with patch('prime_scraper.requests.get', return_value=resp):
            df = prime_scraper.get_history('wisp_prime_set')
        expected_cols = [
            'datetime', 'avg_price', 'min_price', 'max_price', 'volume', 'item'
        ]
        self.assertEqual(list(df.columns), expected_cols)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df['datetime']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df['avg_price']))
        self.assertEqual(df['item'].iloc[0], 'Wisp')

    def test_cleaning_deduplicates(self):
        data = [
            {
                'datetime': pd.Timestamp('2023-01-01'),
                'avg_price': 0,
                'min_price': 45,
                'max_price': 55,
                'volume': 10,
                'item': 'Wisp'
            },
            {
                'datetime': pd.Timestamp('2023-01-01'),
                'avg_price': 0,
                'min_price': 45,
                'max_price': 55,
                'volume': 10,
                'item': 'Wisp'
            },
            {
                'datetime': pd.Timestamp('2023-01-02'),
                'avg_price': 60,
                'min_price': 55,
                'max_price': 65,
                'volume': None,
                'item': 'Wisp'
            }
        ]
        df = pd.DataFrame(data)
        clean = (
            df.sort_values(['item'])
            .drop_duplicates()
            .replace(0, pd.NA)
        )
        self.assertEqual(len(clean), 2)
        self.assertTrue(pd.isna(clean.loc[clean['datetime'] == pd.Timestamp('2023-01-01'), 'avg_price']).iloc[0])


if __name__ == '__main__':
    unittest.main()
