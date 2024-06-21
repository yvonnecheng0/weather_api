import unittest
from unittest.mock import patch
from weather import fetch_weather_data
from weather import convert_to_dataframe
from weather import save_to_database
from weather import query_database
import pandas as pd
import sqlalchemy as db


class TestWeather(unittest.TestCase):
    def test_fetch_weather_data(self):
        api_key = 'fake_api_key'
        city = 'London'
        # Mock the requests.get call to return a fake response
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                'name': 'London',
                'main': {'temp': 15},
                'weather': [{'description': 'clear sky'}]
            }
            weather_data = fetch_weather_data(api_key, city)
            self.assertEqual(weather_data['City'], 'London')
            self.assertEqual(weather_data['Temperature'], 15)
            self.assertEqual(weather_data['Weather'], 'clear sky')

    def test_convert_to_dataframe(self):
        data = {'City': 'London', 'Temperature': 15, 'Weather': 'clear sky'}
        df = convert_to_dataframe(data)
        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertEqual(df.iloc[0]['City'], 'London')
        self.assertEqual(df.iloc[0]['Temperature'], 15)
        self.assertEqual(df.iloc[0]['Weather'], 'clear sky')

    def test_save_to_database_and_query(self):
        data = {'City': 'London', 'Temperature': 15, 'Weather': 'clear sky'}
        df = convert_to_dataframe(data)
        engine = save_to_database(df, 'test_weather_data', 'weather')
        results = query_database(engine, 'weather')
        self.assertEqual(results.iloc[0]['City'], 'London')
        self.assertEqual(results.iloc[0]['Temperature'], 15)
        self.assertEqual(results.iloc[0]['Weather'], 'clear sky')


if __name__ == '__main__':
    unittest.main()
