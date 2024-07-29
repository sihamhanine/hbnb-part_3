import unittest
from flask import Flask
from flask.testing import FlaskClient
from api.country_api import country_api
from models.country import Country
from unittest.mock import patch, MagicMock
import json
import pycountry

class CountryApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(country_api)
        self.app.testing = True
        self.client = self.app.test_client()
        self.client: FlaskClient

    @patch('api.country_api.pycountry.countries')
    def test_get_all_countries(self, mock_pycountry_countries):
        mock_pycountry_countries = [
            MagicMock(name='Country1', alpha_2='C1'),
            MagicMock(name='Country2', alpha_2='C2')
        ]

        with patch('api.country_api.pycountry.countries', mock_pycountry_countries):
            response = self.client.get('/countries')

        expected_countries = [
            {'name': 'Country1', 'alpha_2': 'C1'},
            {'name': 'Country2', 'alpha_2': 'C2'}
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), expected_countries)

    @patch('api.country_api.pycountry.countries')
    def test_get_country(self, mock_pycountry_countries):
        mock_country = MagicMock(name='Country1', alpha_2='C1')
        mock_pycountry_countries.get.return_value = mock_country

        response = self.client.get('/countries/C1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'name': 'Country1', 'alpha_2': 'C1'})

    @patch('api.country_api.pycountry.countries')
    def test_get_country_not_found(self, mock_pycountry_countries):
        mock_pycountry_countries.get.return_value = None

        response = self.client.get('/countries/C1')

        self.assertEqual(response.status_code, 404)
        self.assertIn('Country not found', response.get_json()['error'])

    @patch('api.country_api.pycountry.countries')
    def test_get_country_cities(self, mock_pycountry_countries):
        mock_country = MagicMock(name='Country1', alpha_2='C1')
        mock_pycountry_countries.get.return_value = mock_country

        mock_cities = [
            {"id": "c1", "city": ["City1", "City2"]}
        ]

        with patch('builtins.open', unittest.mock.mock_open(read_data=json.dumps(mock_cities))):
            response = self.client.get('/countries/C1/cities')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), ["City1", "City2"])

    @patch('api.country_api.pycountry.countries')
    def test_get_country_cities_not_found(self, mock_pycountry_countries):
        mock_country = MagicMock(name='Country1', alpha_2='C1')
        mock_pycountry_countries.get.return_value = mock_country

        mock_cities = [
            {"id": "c2", "city": ["City1", "City2"]}
        ]

        with patch('builtins.open', unittest.mock.mock_open(read_data=json.dumps(mock_cities))):
            response = self.client.get('/countries/C1/cities')

        self.assertEqual(response.status_code, 404)
        self.assertIn('Cities not found', response.get_json()['error'])

    @patch('api.country_api.pycountry.countries')
    def test_get_country_cities_country_not_found(self, mock_pycountry_countries):
        mock_pycountry_countries.get.return_value = None

        response = self.client.get('/countries/C1/cities')

        self.assertEqual(response.status_code, 404)
        self.assertIn('Country not found', response.get_json()['error'])

if __name__ == '__main__':
    unittest.main()
