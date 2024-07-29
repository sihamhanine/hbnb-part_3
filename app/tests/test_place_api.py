import unittest
from flask import Flask
from flask.testing import FlaskClient
from api.place_api import place_api
from models.place import Place
from persistence.datamanager import DataManager
from unittest.mock import patch, MagicMock
import json

class PlaceApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(place_api)
        self.app.testing = True
        self.client = self.app.test_client()
        self.client: FlaskClient

    @patch('api.place_api.DataManager')
    def test_add_place_success(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.save.return_value = None

        response = self.client.post('/places', json={
            "name": "Test Place",
            "description": "A beautiful place",
            "address": "123 Test St",
            "latitude": 12.34,
            "longitude": 56.78,
            "num_rooms": 3,
            "num_bathrooms": 2,
            "price_per_night": 100.0,
            "max_guests": 4,
            "host_id": "host1",
            "city_id": "city1"
        })

        self.assertEqual(response.status_code, 201)
        self.assertIn('Place added', response.get_json()['Success'])

    @patch('api.place_api.DataManager')
    def test_add_place_missing_field(self, MockDataManager):
        response = self.client.post('/places', json={
            "name": "Test Place",
            "description": "A beautiful place"
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required field', response.get_json()['Error'])

    @patch('api.place_api.DataManager')
    def test_add_place_invalid_field_type(self, MockDataManager):
        response = self.client.post('/places', json={
            "name": "Test Place",
            "description": "A beautiful place",
            "address": "123 Test St",
            "latitude": "invalid_latitude",
            "longitude": 56.78,
            "num_rooms": 3,
            "num_bathrooms": 2,
            "price_per_night": 100.0,
            "max_guests": 4,
            "host_id": "host1",
            "city_id": "city1"
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('TypeError', response.get_json()['Error'])

    @patch('api.place_api.DataManager')
    def test_get_places(self, MockDataManager):
        with patch('builtins.open', unittest.mock.mock_open(read_data='[{"name": "Test Place"}]')):
            response = self.client.get('/places')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), [{"name": "Test Place"}])

    @patch('api.place_api.DataManager')
    def test_get_places_file_not_found(self, MockDataManager):
        with patch('builtins.open', side_effect=FileNotFoundError):
            response = self.client.get('/places')

            self.assertEqual(response.status_code, 404)
            self.assertIn('No place found', response.get_json()['Error'])

    @patch('api.place_api.DataManager')
    def test_get_place_by_id(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.get.return_value = {
            "name": "Test Place",
            "description": "A beautiful place"
        }

        response = self.client.get('/places/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            "name": "Test Place",
            "description": "A beautiful place"
        })

    @patch('api.place_api.DataManager')
    def test_get_place_by_id_not_found(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.get.return_value = None

        response = self.client.get('/places/1')

        self.assertEqual(response.status_code, 404)
        self.assertIn('Place not found', response.get_json()['Error'])

    @patch('api.place_api.DataManager')
    def test_delete_place_not_found(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.get.return_value = None

        response = self.client.delete('/places/1')

        self.assertEqual(response.status_code, 404)
        self.assertIn('Place not found', response.get_json()['Error'])

    @patch('api.place_api.DataManager')
    def test_update_place(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.get.return_value = {
            "name": "Test Place",
            "description": "A beautiful place",
            "address": "123 Test St",
            "latitude": 12.34,
            "longitude": 56.78,
            "num_rooms": 3,
            "num_bathrooms": 2,
            "price_per_night": 100.0,
            "max_guests": 4,
            "host_id": "host1",
            "city_id": "city1"
        }

        response = self.client.put('/places/1', json={
            "name": "Updated Place",
            "description": "An updated beautiful place",
            "address": "123 Test St",
            "latitude": 12.34,
            "longitude": 56.78,
            "num_rooms": 3,
            "num_bathrooms": 2,
            "price_per_night": 150.0,
            "max_guests": 4,
            "host_id": "host1",
            "city_id": "city1"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('Place updated', response.get_json()['Success'])

    @patch('api.place_api.DataManager')
    def test_update_place_not_found(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.get.return_value = None

        response = self.client.put('/places/1', json={
            "name": "Updated Place",
            "description": "An updated beautiful place",
            "address": "123 Test St",
            "latitude": 12.34,
            "longitude": 56.78,
            "num_rooms": 3,
            "num_bathrooms": 2,
            "price_per_night": 150.0,
            "max_guests": 4,
            "host_id": "host1",
            "city_id": "city1"
        })

        self.assertEqual(response.status_code, 404)
        self.assertIn('Place not found', response.get_json()['Error'])

if __name__ == '__main__':
    unittest.main()
