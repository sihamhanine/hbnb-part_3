import unittest
from flask import Flask
from flask.testing import FlaskClient
from api.cities_api import cities_api
from models.city import City
from unittest.mock import patch, MagicMock
import json
import datetime
import os

class CitiesApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(cities_api)
        self.app.testing = True
        self.client = self.app.test_client()
        self.client: FlaskClient

    @patch('os.path.exists')
    @patch('builtins.open')
    def test_create_city(self, mock_open, mock_path_exists):
        mock_path_exists.return_value = True
        city_data = {'id': 'country1', 'name': 'City1'}
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps([{'id': 'country1', 'city': []}])

        response = self.client.post('/cities', json=city_data)

        self.assertEqual(response.status_code, 201)
        self.assertIn('City added', response.get_json()['Success'])

    @patch('os.path.exists')
    @patch('builtins.open')
    def test_create_city_invalid_data(self, mock_open, mock_path_exists):
        mock_path_exists.return_value = True
        city_data = {'id': '', 'name': ''}

        response = self.client.post('/cities', json=city_data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid data', response.get_json()['Error'])

    @patch('os.path.exists')
    @patch('builtins.open')
    def test_create_existing_city(self, mock_open, mock_path_exists):
        mock_path_exists.return_value = True
        city_data = {'id': 'country1', 'name': 'City1'}
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps([{'id': 'country1', 'city': [{'name': 'City1'}]}])

        response = self.client.post('/cities', json=city_data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('City already exists', response.get_json()['Error'])

    @patch('builtins.open')
    def test_get_all_cities(self, mock_open):
        mock_cities = [{'id': 'country1', 'city': [{'name': 'City1'}, {'name': 'City2'}]}]
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(mock_cities)

        response = self.client.get('/cities')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), mock_cities)

    @patch('builtins.open')
    def test_get_city(self, mock_open):
        mock_cities = [{'id': 'country1', 'city': [{'uniq_id': 'city1', 'name': 'City1'}, {'uniq_id': 'city2', 'name': 'City2'}]}]
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(mock_cities)

        response = self.client.get('/cities/city1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'uniq_id': 'city1', 'name': 'City1'})

    @patch('builtins.open')
    def test_get_city_not_found(self, mock_open):
        mock_cities = [{'id': 'country1', 'city': [{'uniq_id': 'city1', 'name': 'City1'}, {'uniq_id': 'city2', 'name': 'City2'}]}]
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(mock_cities)

        response = self.client.get('/cities/city3')

        self.assertEqual(response.status_code, 404)
        self.assertIn('City not found', response.get_json()['Error'])

    @patch('builtins.open')
    def test_update_city(self, mock_open):
        mock_cities = [{'id': 'country1', 'city': [{'uniq_id': 'city1', 'name': 'City1'}]}]
        updated_city_data = {'name': 'UpdatedCity1'}
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(mock_cities)

        response = self.client.put('/cities/city1', json=updated_city_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('City updated', response.get_json()['Success'])

    @patch('builtins.open')
    def test_delete_city(self, mock_open):
        mock_cities = [{'id': 'country1', 'city': [{'uniq_id': 'city1', 'name': 'City1'}]}]
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(mock_cities)

        response = self.client.delete('/cities/city1')

        self.assertEqual(response.status_code, 200)
        self.assertIn('City deleted', response.get_json()['Success'])

    @patch('builtins.open')
    def test_delete_city_not_found(self, mock_open):
        mock_cities = [{'id': 'country1', 'city': [{'uniq_id': 'city1', 'name': 'City1'}]}]
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(mock_cities)

        response = self.client.delete('/cities/city2')

        self.assertEqual(response.status_code, 404)
        self.assertIn('City not found', response.get_json()['Error'])

if __name__ == '__main__':
    unittest.main()
