import unittest
from flask import Flask
from flask.testing import FlaskClient
from api.amenities_api import amenities_api
from models.amenity import Amenity
from persistence.datamanager import DataManager
from unittest.mock import patch, MagicMock
import json

class AmenitiesApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(amenities_api)
        self.app.testing = True 
        self.client = self.app.test_client()
        self.client: FlaskClient

    @patch('api.amenities_api.DataManager')
    def test_add_amenity_success(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.save.return_value = None

        response = self.client.post('/amenities', json={'name': 'Pool'})

        self.assertEqual(response.status_code, 201)

    @patch('api.amenities_api.DataManager')
    def test_add_amenity_missing_field(self, MockDataManager):
        response = self.client.post('/amenities', json={'name': ''})

        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required field', response.get_json()['Error'])

    @patch('api.amenities_api.DataManager')
    def test_add_amenity_already_exists(self, MockDataManager):
        with patch('builtins.open', unittest.mock.mock_open(read_data='[{"name": "Pool"}]')):
            response = self.client.post('/amenities', json={'name': 'Pool'})

        self.assertEqual(response.status_code, 409)
        self.assertIn('Amenity already exists', response.get_json()['Error'])

    @patch('api.amenities_api.DataManager')
    def test_get_amenities_success(self, mock_open):
        response = self.client.get('/amenities')

        self.assertEqual(response.status_code, 200)

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_get_amenities_not_found(self, mock_open):
        response = self.client.get('/amenities')

        self.assertEqual(response.status_code, 404)
        self.assertIn('No amenity found', response.get_json()['Error'])

    @patch('api.amenities_api.DataManager')
    def test_get_amenity_not_found(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.get.return_value = None

        response = self.client.get('/amenities/1')

        self.assertEqual(response.status_code, 404)
        self.assertIn('Amenity not found', response.get_json()['Error'])

    @patch('api.amenities_api.DataManager')
    def test_delete_amenity_not_found(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.get.return_value = None

        response = self.client.delete('/amenities/1')

        self.assertEqual(response.status_code, 404)
        self.assertIn('Amenity not found', response.get_json()['Error'])



    @patch('api.amenities_api.DataManager')
    def test_update_amenity(self, MockDataManager):
        with open("data/Amenity.json", 'r') as f:
            users = json.load(f)
            for user in users:
                if user.get("name") == "Pool":
                    id = user.get("uniq_id")

        response = self.client.put(f'/amenities/{id}', json={'name': 'Gym'})

        self.assertEqual(response.status_code, 200)

    @patch('api.amenities_api.DataManager')
    def test_update_amenity_not_found(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.get.return_value = None

        response = self.client.put('/amenities/1', json={'name': 'Gym'})

        self.assertEqual(response.status_code, 404)

    @patch('api.amenities_api.DataManager')
    def test_delete_amenity_success(self, MockDataManager):
        with open("data/Amenity.json", 'r') as f:
            users = json.load(f)
            for user in users:
                if user.get("name") == "Pool":
                    id = user.get("uniq_id")

        response = self.client.delete(f'/amenities/{id}')

        self.assertEqual(response.status_code, 200)
        self.assertIn('Amenity deleted', response.get_json()['Success'])

if __name__ == '__main__':
    unittest.main()
